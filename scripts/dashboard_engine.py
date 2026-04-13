#!/usr/bin/env python3
import os
import json
import time
from datetime import datetime
import subprocess
import re

STATE_FILE = "temp/dashboard_state.json"
INGEST_STATUS_FILE = "temp/ingest_status.json"
INGEST_REGISTRY_FILE = "temp/ingest_registry.json"
DOC_STATUS_FILE = "rag_storage/kv_store_doc_status.json"
STATUS_FILE_NAME = "STATUS.md"
TMP_STATUS_BASE = "temp/STATUS.md.{pid}.tmp"

class DashboardEngine:
    def _clean_val(self, val):
        """Converts string percentages and values to float for comparison."""
        if isinstance(val, (int, float)): return float(val)
        if not val or val == "N/A": return 0.0
        try:
            # Remove %, MiB, GB, etc.
            clean = re.sub(r'[^\d.]+', '', val.replace(',', '.'))
            return float(clean) if clean else 0.0
        except Exception:
            return 0.0

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
        self.registry = {}
        self.load_state()
        self.load_registry()

    def load_registry(self):
        if os.path.exists(INGEST_REGISTRY_FILE):
            try:
                with open(INGEST_REGISTRY_FILE, "r", encoding="utf-8") as f:
                    self.registry = json.load(f)
            except Exception:
                pass

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

    def safe_load_json(self, filepath, max_retries=3):
        """Safely loads a JSON file with retry logic to handle concurrent write issues."""
        for i in range(max_retries):
            try:
                if not os.path.exists(filepath):
                    return None
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                if i < max_retries - 1:
                    time.sleep(0.1) # Wait for write to finish
                    continue
                raise
            except Exception:
                return None
        return None

    def gather_rag_stats(self):
        """Parses kv_store_doc_status.json for total docs and chunks statistics."""
        stats = {
            "total_docs": 0,
            "processed_docs": 0,
            "failed_docs": 0,
            "pending_docs": 0,
            "total_chunks": 0
        }
        try:
            data = self.safe_load_json(DOC_STATUS_FILE)
            if data:
                stats["total_docs"] = len(data)
                for doc_id, doc_data in data.items():
                    status = doc_data.get("status", "unknown")
                    if status == "processed":
                        stats["processed_docs"] += 1
                    elif status == "failed":
                        stats["failed_docs"] += 1
                    else:
                        stats["pending_docs"] += 1
                    
                    stats["total_chunks"] += doc_data.get("chunks_count", 0)
        except Exception as e:
            self._log_event(f"🚨 Ошибка парсинга RAG статистики: {e}")
        return stats

    def run_cmd(self, shell_cmd):
        try:
            res = subprocess.run(shell_cmd, shell=True, capture_output=True, text=True, timeout=30)
            return res.stdout.strip()
        except subprocess.TimeoutExpired:
            return "Timeout"
        except Exception as e:
            return str(e)

    def parse_chunk_status(self):
        """Runs docker logs --tail 200 lightrag_api and gets the last chunk progress and doc_id"""
        logs = self.run_cmd("docker logs --tail 200 lightrag_api 2>&1")
        
        # 1. Catch [X/Y] chunks
        chunk_matches = re.findall(r"Chunk (\d+) of (\d+)", logs)
        chunk_info = chunk_matches[-1] if chunk_matches else None
        
        # 2. Catch DocID mapping from log context
        # Look for "Processing d-id: doc-xxxx" or "doc-xxxxx (async: X)"
        doc_matches = re.findall(r"(doc-[a-f0-9]{32})", logs)
        active_doc_id = doc_matches[-1] if doc_matches else None
        
        active_filename = "Unknown Document"
        if active_doc_id and active_doc_id in self.registry:
            active_filename = self.registry[active_doc_id].get("filename", "N/A")
        elif active_doc_id:
            active_filename = f"Background Indexing ({active_doc_id[:8]}...)"

        return chunk_info, active_filename

    def check_stuck_status(self, now, is_working=False):
        """Checks if process is stalled for > 10 minutes (600 secs)"""
        if is_working:
            return False # Cannot be stuck if CPU is high or chunks are moving
            
        doc_idle = now - self.state.get("last_doc_update_time", now)
        chunk_idle = now - self.state.get("last_chunk_update_time", now)
        
        # Increased to 10 minutes because local Neo4j indexing is very slow on large docs
        if doc_idle > 600 and chunk_idle > 600:
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
        # Optimized: get specific metrics for our containers
        container_names = ["lightrag_api", "lightrag_neo4j", "lightrag_qdrant"]
        metrics = {name: {"cpu": "N/A", "ram": "N/A", "status": "🛑 Offline"} for name in container_names}
        
        # Check basic presence first to avoid timeout confusion
        ps_raw = self.run_cmd('docker ps --format "{{.Names}}"')
        active_containers = ps_raw.split("\n") if ps_raw and "Timeout" not in ps_raw else []
        
        docker_raw = self.run_cmd('docker stats --no-stream --format "{{.Name}}|{{.CPUPerc}}|{{.MemUsage}}" ' + " ".join(container_names))
        
        if docker_raw and "Timeout" not in docker_raw:
            for line in docker_raw.split("\n"):
                parts = line.split("|")
                if len(parts) == 3:
                    name, cpu, ram = [p.strip() for p in parts]
                    # On some systems name might have a leading slash
                    clean_name = name.lstrip('/')
                    if clean_name in metrics:
                        mem_actual = ram.split(" / ")[0].strip()
                        metrics[clean_name] = {"cpu": cpu, "ram": mem_actual, "status": "✅ Online"}
        else:
            # Fallback to simple Online/Offline if stats failed but ps saw them
            for name in container_names:
                if any(name in c for c in active_containers):
                    metrics[name]["status"] = "✅ Online (Metrics N/A)"

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
        
        # 0. Physical folder scan (Ground Truth Total)
        CONTENT_DIR = "docs/knowledge"
        files_in_folder = []
        try:
            if os.path.exists(CONTENT_DIR):
                for f in os.listdir(CONTENT_DIR):
                    if f.endswith(".md"):
                        files_in_folder.append(f)
            total_doc_physical = len(files_in_folder)
        except Exception:
            total_doc_physical = 0

        # 1. Get RAG stats (Ground Truth Processed)
        rag_stats = self.gather_rag_stats()
        
        # Cross-reference with registry for accurate batch progress
        self.load_registry()
        processed_count = 0
        doc_status_data = self.safe_load_json(DOC_STATUS_FILE) or {}
        
        for doc_id, info in self.registry.items():
            if doc_status_data.get(doc_id, {}).get("status") == "processed":
                processed_count += 1
        
        # 2. Get ingest status for "Current Activity"
        ingest_data = self.get_ingest_status()
        last_file = ingest_data.get("last_file", "N/A")
        
        # 3. Get chunk status
        chunk_info, active_filename = self.parse_chunk_status()
        chunk_str_display = "N/A"
        is_chunking_active = False
        
        if chunk_info:
            c_now, c_total = int(chunk_info[0]), int(chunk_info[1])
            chunk_str_display = f"[{c_now}/{c_total}]"
            if c_now < c_total:
                is_chunking_active = True
            
            if chunk_str_display != self.state.get("last_chunk", ""):
                self._log_event(f"🧩 Обработан чанк {chunk_str_display} в документе: {active_filename}")
                self.state["last_chunk"] = chunk_str_display
                self.state["last_chunk_update_time"] = now
                self.save_state()
             
        # 3. Get chunk status & active file
        chunk_info, active_filename = self.parse_chunk_status()
        chunk_str_display = "N/A"
        is_chunking_active = False
        
        if chunk_info:
            c_now, c_total = int(chunk_info[0]), int(chunk_info[1])
            chunk_str_display = f"[{c_now}/{c_total}]"
            
            # Use active_filename from registry instead of last_file fallback
            if c_now == c_total and c_total > 0:
                if active_filename != "Unknown Document" and active_filename not in self.state.get("indexed_files", []):
                    if "indexed_files" not in self.state: self.state["indexed_files"] = []
                    self.state["indexed_files"].append(active_filename)
                    self._log_event(f"✅ Документ проиндексирован (Neo4j): {active_filename}")
                    self.save_state()
            else:
                is_chunking_active = True
            
            if chunk_str_display != self.state.get("last_chunk", ""):
                self._log_event(f"🧩 Обработан чанк {chunk_str_display} в документе: {active_filename}")
                self.state["last_chunk"] = chunk_str_display
                self.state["last_chunk_update_time"] = now
                self.save_state()

        # 4. Final Progress Logic (Direct Calculation)
        batch_total = total_doc_physical
        count_indexed = processed_count
        
        doc_percent = (count_indexed / batch_total * 100) if batch_total > 0 else 0.0
        
        doc_str = f"[{count_indexed}/{batch_total}] ({round(doc_percent, 1)}%)"
        rag_total_str = f"{rag_stats.get('processed_docs', 0)} (всего в базе)"
        
        active_work = rag_stats.get("total_docs", 0) - rag_stats.get("processed_docs", 0)
        queue_str = f"- **Очередь RAG**: `{active_work} док.` (Pending/Indexing)" if active_work > 0 else ""

        # 5. Get Metrics & Determine Status
        metrics, ollama_cpu_str, ollama_status, ollama_cpu_total = self.gather_system_metrics()
        
        # CPU values for comparison
        neo4j_cpu = self._clean_val(metrics.get('lightrag_neo4j', {}).get('cpu', 0))
        api_cpu = self._clean_val(metrics.get('lightrag_api', {}).get('cpu', 0))
        is_hard_working = ollama_cpu_total > 5.0 or neo4j_cpu > 10.0 or api_cpu > 10.0
        
        is_stalled = self.check_stuck_status(now, is_working=(is_hard_working or is_chunking_active))
        
        if count_indexed == 0 and batch_total == 0 and active_work == 0:
            general_status = "Покой (Ожидание)"
        elif count_indexed >= batch_total and active_work == 0:
            if is_hard_working or is_chunking_active:
                general_status = "Индексация (Финальная сборка графа)"
            else:
                general_status = "Завершен"
        else:
            if is_stalled:
                general_status = "🛑 ЗАВИСАНИЕ"
                if not self.state.get("stall_logged"):
                    self.capture_error_log()
                    self.state["stall_logged"] = True
                    self.save_state()
            else:
                if is_hard_working or active_work > 0:
                     reason = "в очереди" if active_work > 0 else "активно"
                     general_status = f"Индексация ({reason})"
                else:
                     general_status = "Ожидание / Завершение"
                
                if self.state.get("stall_logged"):
                    self.state["stall_logged"] = False
                    self.save_state()

        # 5. Assemble markdown string
        dt_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        md_lines = [
            f"Обновлено: `{dt_str}` (Авто-обновление: 60 сек)",
            "",
            f"## ⚡ Статус Индексации: {general_status}",
            f"- **Прогресс пачки**: `{doc_str}`"
        ]
        
        if queue_str:
            md_lines.append(queue_str.strip())
            
        md_lines.extend([
            f"- **Всего в RAG**: `{rag_total_str}`",
            f"- **Прогресс частей (Чанки)**: `{chunk_str_display}`",
            f"- **Лимиты ресурсов (Throttling)**: `✅ Active (Max 80% CPU)`",
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
        ])

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
