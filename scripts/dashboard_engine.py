#!/usr/bin/env python3
import os
import json
import time
from datetime import datetime
import subprocess
import re

STATE_FILE = "temp/dashboard_state.json"
INGEST_STATUS_FILE = "temp/ingest_status.json"
STATUS_FILE_NAME = "STATUS.md"
TMP_STATUS_FILE_NAME = "temp/STATUS.md.tmp"

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
                self._log_event(f"🚨 ERROR LOG: {line.strip()}")

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
        
        # 0. Physical folder scan (B - Total Docs)
        CONTENT_DIR = "docs/notebook_content"
        try:
            # Get all .md files in the folder
            files_in_folder = [f for f in os.listdir(CONTENT_DIR) if f.endswith(".md")]
            total_doc_physical = len(files_in_folder)
        except Exception:
            files_in_folder = []
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
        # Ensure we only count indexed files that are ACTIVE in the folder (not deleted)
        current_indexed_list = [f for f in self.state.get("indexed_files", []) if f in files_in_folder]
        count_indexed = len(current_indexed_list)
        
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
        
        # Assemble markdown string
        dt_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        md_lines = [
            f"Обновлено: `{dt_str}` (Авто-обновление: 60 сек)",
            "",
            f"## ⚡ Статус Индексации: {general_status}",
            f"- **Реальная обработка (Neo4j)**: `{doc_str}`",
            f"- **Прогресс частей (Чанки)**: `{chunk_str_display}`",
            f"- **Активность LLM (GPU/Ollama)**: {ollama_status}",
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

        # Write atomically
        content = "\n".join(md_lines)
        with open(TMP_STATUS_FILE_NAME, "w", encoding="utf-8") as f:
            f.write(content)
            
        os.rename(TMP_STATUS_FILE_NAME, STATUS_FILE_NAME)

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
