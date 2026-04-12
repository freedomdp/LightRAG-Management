#!/usr/bin/env python3
import os
import json
import time
from datetime import datetime
import subprocess
import re

STATE_FILE = "temp/dashboard_state.json"
INGEST_STATUS_FILE = "temp/ingest_status.json"
DOC_STATUS_FILE = "rag_storage/kv_store_doc_status.json"
STATUS_FILE_NAME = "STATUS.md"
TMP_STATUS_BASE = "temp/STATUS.md.{pid}.tmp"

class DashboardEngine:
    def __init__(self):
        self.state = {
            "journal": [],
            "last_doc_current": 0,
            "last_doc_name": "",
            "last_chunk": "",
            "last_doc_update_time": time.time(),
            "last_chunk_update_time": time.time(),
            "stall_logged": False
        }
        self.load_state()

    def load_state(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Merge carefully avoiding overwriting initial keys if they are missing
                    for k, v in data.items():
                        self.state[k] = v
            except Exception as e:
                self._log_event(f"🚨 Ошибка загрузки state: {e}")

    def save_state(self):
        # Truncate journal to 100 entries to prevent infinite growth
        if len(self.state["journal"]) > 100:
            self.state["journal"] = self.state["journal"][:100]
        
        try:
            os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.state, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _log_event(self, message):
        """Adds a message to the top of the journal with a timestamp."""
        ts = datetime.now().strftime("[%H:%M:%S]")
        self.state["journal"].insert(0, f"{ts} {message}")
        self.save_state()

    def get_ingest_status(self):
        try:
            if os.path.exists(INGEST_STATUS_FILE):
                with open(INGEST_STATUS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return {"current": 0, "total": 0, "last_file": "N/A", "timestamp": 0}

    def gather_rag_stats(self):
        """Parses kv_store_doc_status.json for total dots and chunks statistics."""
        stats = {
            "total_docs": 0,
            "processed_docs": 0,
            "failed_docs": 0,
            "total_chunks": 0
        }
        if os.path.exists(DOC_STATUS_FILE):
            try:
                with open(DOC_STATUS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    stats["total_docs"] = len(data)
                    for doc_id, doc_data in data.items():
                        status = doc_data.get("status", "unknown")
                        if status == "processed":
                            stats["processed_docs"] += 1
                        elif status == "failed":
                            stats["failed_docs"] += 1
                        
                        stats["total_chunks"] += doc_data.get("chunks_count", 0)
            except Exception as e:
                self._log_event(f"🚨 Ошибка парсинга RAG статистики: {e}")
        return stats

    def run_cmd(self, shell_cmd):
        try:
            res = subprocess.run(shell_cmd, shell=True, capture_output=True, text=True, timeout=10)
            return res.stdout.strip()
        except subprocess.TimeoutExpired:
            return "Timeout"
        except Exception as e:
            return str(e)

    def parse_chunk_status(self):
        """Runs docker logs --tail 100 lightrag_api and gets the last chunk progress"""
        logs = self.run_cmd("docker logs --tail 100 lightrag_api 2>&1")
        # Find all chunks, extract the last one
        matches = re.findall(r"Chunk (\d+) of (\d+)", logs)
        if matches:
            return matches[-1] # tuple ('X', 'Y')
        return None

    def check_stuck_status(self, now):
        """Checks if process is stalled for > 5 minutes (300 secs)"""
        doc_idle = now - self.state.get("last_doc_update_time", now)
        chunk_idle = now - self.state.get("last_chunk_update_time", now)
        
        if doc_idle > 300 and chunk_idle > 300:
            return True
        return False

    def capture_error_log(self):
        """Tail 10 docker logs of lightrag_api when stalled to push to journal."""
        logs = self.run_cmd("docker logs --tail 10 lightrag_api 2>&1")
        lines = logs.split("\n")
        # log each line as error to journal
        for line in reversed(lines):
            if line.strip():
                # Don't label INFO logs as ERROR
                prefix = "🚨 ERROR LOG:" if "INFO:" not in line else "📜 API LOG:"
                self._log_event(f"{prefix} {line.strip()}")

    def gather_system_metrics(self):
        # 1. Docker metrics
        docker_raw = self.run_cmd('docker stats --no-stream --format "{{.Name}}|{{.CPUPerc}}|{{.MemUsage}}" lightrag_api lightrag_neo4j lightrag_qdrant')
        metrics = {"lightrag_api": {"cpu": "N/A", "ram": "N/A", "status": "🛑 Offline"},
                   "lightrag_neo4j": {"cpu": "N/A", "ram": "N/A", "status": "🛑 Offline"},
                   "lightrag_qdrant": {"cpu": "N/A", "ram": "N/A", "status": "🛑 Offline"}}
        
        if docker_raw and "Timeout" not in docker_raw:
            for line in docker_raw.split("\n"):
                parts = line.split("|")
                if len(parts) == 3:
                    name, cpu, ram = parts
                    mem_actual = ram.split(" / ")[0]  # Extracts basically just the used format like 485.7MiB
                    metrics[name] = {"cpu": cpu, "ram": mem_actual, "status": "✅ Online"}

        # 2. Ollama metrics
        ollama_ps = self.run_cmd('ps -A -o %cpu,command | grep ollama | grep -v grep')
        ollama_cpu_total = 0.0
        for line in ollama_ps.split("\n"):
            line = line.strip()
            if line:
                try:
                    cpu_val = float(line.split()[0].replace(',', '.'))
                    ollama_cpu_total += cpu_val
                except Exception:
                    pass
        ollama_cpu_str = f"{ollama_cpu_total:.2f}%"
        ollama_status = "✅ Active" if ollama_cpu_total >= 1.0 else "💤 LLM простаивает"

        return metrics, ollama_cpu_str, ollama_status, ollama_cpu_total

    def build_dashboard(self):
        now = time.time()
        
        # 0. Physical folder scan (B - Total Docs) - RECURSIVE
        CONTENT_DIR = "docs/notebook_content"
        files_in_folder = []
        try:
            for root, dirs, files in os.walk(CONTENT_DIR):
                for file in files:
                    if file.endswith(".md"):
                        rel_path = os.path.relpath(os.path.join(root, file), CONTENT_DIR)
                        files_in_folder.append(rel_path)
            total_doc_physical = len(files_in_folder)
        except Exception:
            total_doc_physical = 0

        # 1. Get ingest status (to know what file is active)
        ingest_data = self.get_ingest_status()
        last_file = ingest_data.get("last_file", "N/A")
        
        # 2. Get chunk status and update Indexed List (A)
        chunk_data = self.parse_chunk_status()
        chunk_str_display = "N/A"
        is_chunking_active = False
        
        if chunk_data:
            c_now, c_total = int(chunk_data[0]), int(chunk_data[1])
            chunk_str_display = f"[{c_now}/{c_total}]"
            
            # Check if current file just finished its chunks
            if c_now == c_total and c_total > 0:
                if last_file != "N/A" and last_file not in self.state.get("indexed_files", []):
                    if "indexed_files" not in self.state:
                        self.state["indexed_files"] = []
                    self.state["indexed_files"].append(last_file)
                    self._log_event(f"✅ Документ полностью проиндексирован (Neo4j): {last_file}")
                    self.save_state()
            elif c_now < c_total:
                is_chunking_active = True
            
            if chunk_str_display != self.state.get("last_chunk", ""):
                self._log_event(f"🧩 Обработан чанк {chunk_str_display} в текущем документе")
                self.state["last_chunk"] = chunk_str_display
                self.state["last_chunk_update_time"] = now
                self.save_state()

        # 3. Calculate Real Processing (A - Processed)
        rag_stats = self.gather_rag_stats()
        # Optimized: Count how many documents from ANY source are currently in 'processed' state
        # but specifically from the ones we are interested in.
        # However, for simplicity and accuracy, we will count how many unique filenames 
        # from DOC_STATUS_FILE match processed state.
        
        count_indexed = rag_stats.get("processed_docs", 0) - 314 # Baseline check
        if count_indexed < 0: count_indexed = 0
        
        # Or better: track specific IDs we enqueued (future optimization)
        # For now, let's just make it look at the delta or total progress of the folder.
        
        doc_percent = 0.0
        if total_doc_physical > 0:
            doc_percent = (count_indexed / total_doc_physical) * 100
        
        doc_str = f"[{count_indexed}/{total_doc_physical}] ({round(doc_percent, 1)}%)"

        # 3. Detect Stuck / General Status
        is_stalled = self.check_stuck_status(now)
        
        if count_indexed == 0 and total_doc_physical == 0:
            general_status = "Покой (Ожидание)"
        elif count_indexed >= total_doc_physical and total_doc_physical > 0:
            if is_chunking_active:
                general_status = "Индексация (Финальные чанки)"
            else:
                general_status = "Завершение"
        else:
            if is_stalled:
                general_status = "🛑 ЗАВИСАНИЕ (Требуется вмешательство)"
                if not self.state.get("stall_logged"):
                    self.capture_error_log()
                    self.state["stall_logged"] = True
                    self.save_state()
            else:
                general_status = "Индексация"
                if self.state.get("stall_logged"):
                    self.state["stall_logged"] = False
                    self.save_state()

        # 4. System Metrics
        metrics, ollama_cpu_str, ollama_status, ollama_cpu_val = self.gather_system_metrics()
        
        # 5. Assemble markdown string
        dt_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        md_lines = [
            f"Обновлено: `{dt_str}` (Авто-обновление: 60 сек)",
            "",
            f"## ⚡ Статус Индексации: {general_status}",
            f"- **Реальная обработка (Neo4j)**: `{doc_str}`",
            f"- **Прогресс частей (Чанки)**: `{chunk_str_display}`",
            f"- **Активность LLM (GPU/Ollama)**: {ollama_status}",
            "",
            "",
            "### 🖥️ Системные ресурсы (Docker & Mac)",
            "| Компонент / Контейнер | Нагрузка (CPU %) | RAM / Mem | Статус |",
            "| :--- | :--- | :--- | :--- |",
            f"| **Ollama (Metal GPU)** | {ollama_cpu_str} | N/A | {ollama_status} |",
            f"| **LightRAG API** | {metrics['lightrag_api']['cpu']} | {metrics['lightrag_api']['ram']} | {metrics['lightrag_api']['status']} |",
            f"| **Neo4j DB** | {metrics['lightrag_neo4j']['cpu']} | {metrics['lightrag_neo4j']['ram']} | {metrics['lightrag_neo4j']['status']} |",
            f"| **Qdrant DB** | {metrics['lightrag_qdrant']['cpu']} | {metrics['lightrag_qdrant']['ram']} | {metrics['lightrag_qdrant']['status']} |",
            "",
            "## 📜 Недавняя активность (Самые новые - сверху)"
        ]

        for item in self.state["journal"]:
            md_lines.append(f"- {item}")

        if not self.state["journal"]:
            md_lines.append("- Журнал пуст.")

        # Write atomically using PID to avoid collisions
        content = "\n".join(md_lines)
        tmp_file = TMP_STATUS_BASE.format(pid=os.getpid())
        
        try:
            with open(tmp_file, "w", encoding="utf-8") as f:
                f.write(content)
                
            # os.replace is atomic on Unix/Linux
            os.replace(tmp_file, STATUS_FILE_NAME)
        except Exception as e:
            # If something goes wrong with the temp file, just log it and move on
            if os.path.exists(tmp_file):
                try: os.remove(tmp_file)
                except: pass
            raise e

    def loop(self):
        self._log_event("▶️ Запуск скрипта мониторинга-дашборда V3.0")
        self.build_dashboard() # Первичный быстрый билд
        while True:
            time.sleep(60)
            try:
                self.build_dashboard()
            except Exception as e:
                self._log_event(f"🚨 Внутренняя ошибка скрипта дашборда: {e}")

if __name__ == "__main__":
    engine = DashboardEngine()
    engine.loop()
