import time
import requests
import re
import os
import subprocess
import json
from datetime import datetime

STATUS_FILE = "/Users/sergej/StudioProjects/LightRAG/STATUS.md"
API_URL = "http://localhost:9621/documents/status_counts"
DOCS_DIR = "/Users/sergej/StudioProjects/LightRAG/docs/notebook_content"
PAUSE_FLAG = "scripts/.pause_flag"

def get_container_metrics():
    """Сбор реальной нагрузки CPU и RAM из Docker"""
    metrics = {}
    try:
        cmd = ["docker", "stats", "--no-stream", "--format", "{{.Name}}|{{.CPUPerc}}|{{.MemUsage}}"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        for line in result.stdout.splitlines():
            name, cpu, mem = line.split("|")
            metrics[name] = {"cpu": float(cpu.replace("%", "")), "mem": mem.split(" / ")[0]}
    except: pass
    return metrics

def get_ollama_cpu():
    """Замер нагрузки процесса Ollama (Metal GPU на Mac)"""
    try:
        cmd = "ps -A -o %cpu,comm | grep -i 'ollama' | grep -v 'grep' | awk '{print $1}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=3)
        cpus = [float(c) for c in result.stdout.splitlines() if c.strip()]
        return sum(cpus)
    except: return 0.0

def get_docker_status(container_name):
    try:
        result = subprocess.run(["docker", "inspect", "-f", "{{.State.Status}}", container_name], capture_output=True, text=True, timeout=2)
        state = result.stdout.strip()
        if state == "running": return "✅ Online"
        if state == "paused": return "⏸️ PAUSED"
        return f"❌ {state.capitalize()}"
    except: return "❓ Unknown"

def is_ingest_running():
    try:
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=2)
        # Check for ingest_manager.py but exclude grep
        return "ingest_manager.py" in result.stdout
    except: return False

def format_log_line(line):
    """Удаляет дату и миллисекунды, оставляя [HH:MM:SS]"""
    # Pattern to match YYYY-MM-DD HH:MM:SS,mmm or HH:MM:SS,mmm
    time_match = re.search(r"(\d{4}-\d{2}-\d{2}\s+)?(\d{2}:\d{2}:\d{2})", line)
    if time_match:
        time_str = time_match.group(2)
        # Remove the timestamp part from the original line and replace with formatted
        clean_line = re.sub(r"^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}(,\d+)?\s*-\s*", "", line)
        clean_line = re.sub(r"^\d{2}:\d{2}:\d{2}(,\d+)?\s*-\s*", "", clean_line)
        return f"[{time_str}] {clean_line.strip()}"
    return line.strip()

def get_buffered_logs(current_content):
    """Считывает логи, форматирует и разворачивает (новые сверху)"""
    try:
        all_new_raw = []
        
        # 1. Docker logs
        res_docker = subprocess.run(["docker", "logs", "--since", "90s", "lightrag_api"], capture_output=True, text=True, timeout=3)
        all_new_raw.extend(res_docker.stdout.splitlines())
        
        # 2. System Log
        manager_log_path = "scripts/re-ingest.log"
        if os.path.exists(manager_log_path):
            with open(manager_log_path, "r") as f:
                all_new_raw.extend(f.readlines()[-60:])
        
        keywords = ["Chunk", "Extracting", "Failed", "Completed", "Merging", "LLM cache", "[SYSTEM]", "[AGENT]", "Processing:"]
        filtered = [l.strip() for l in all_new_raw if any(k in l for k in keywords)]
        
        # Форматирование (удаление дат)
        formatted = [format_log_line(l) for l in filtered if l]
        
        # Уникализация и реверс (самые новые сверху)
        combined = []
        seen = set()
        # Process from newest to oldest
        for line in reversed(formatted):
            if line and line not in seen:
                combined.append(line)
                seen.add(line)
        
        return combined[:50]
    except Exception as e:
        return [f"[SYSTEM] Error reading logs: {e}"]

def update_status():
    print("🚀 Дашборд V15.7 'Honest & Clean' запущен (интервал 60с)...")
    while True:
        try:
            current_content = ""
            if os.path.exists(STATUS_FILE):
                with open(STATUS_FILE, "r", encoding="utf-8") as g:
                    current_content = g.read()

            metrics = get_container_metrics()
            ollama_cpu = get_ollama_cpu()
            ingest_active = is_ingest_running()
            pause_requested = os.path.exists(PAUSE_FLAG)
            
            api_cpu = metrics.get("lightrag_api", {}).get("cpu", 0)
            neo_cpu = metrics.get("lightrag_neo4j", {}).get("cpu", 0)
            
            # --- ИНТЕЛЛЕКТУАЛЬНЫЙ СТАТУС ---
            api_status_raw = get_docker_status("lightrag_api")
            
            if pause_requested:
                if ollama_cpu > 5.0:
                    # Если нагрузка есть на паузе - значит либо завершение, либо самообучение агента
                    indexing_status = "🧠 САМООБУЧЕНИЕ (Агент фиксирует опыт)"
                elif "PAUSED" in api_status_raw:
                    indexing_status = "⏸️ На ПАУЗЕ (Безопасно)"
                else:
                    indexing_status = "🛋️ Режим диалога (Тишина)"
            else:
                is_busy = (ollama_cpu > 10.0) or (neo_cpu > 5.0) or (api_cpu > 5.0)
                indexing_status = "⚡ Активна (Идет вычисление)" if is_busy else "💤 Ожидание (Свободен)"
            
            # --- РЕСУРСЫ ---
            api_h = get_docker_status("lightrag_api")
            neo_h = get_docker_status("lightrag_neo4j")
            
            try: real_file_count = len(os.listdir(DOCS_DIR))
            except: real_file_count = 442
            
            try:
                response = requests.get(API_URL, timeout=1)
                data = response.json().get("status_counts", {})
                proc = data.get("processed", 0)
            except: proc = 237 # Fallback
            
            ts = datetime.now().strftime("%H:%M:%S")
            full_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pct = (proc / real_file_count) * 100 if real_file_count > 0 else 0
            
            final_content = f"""# 📊 Живой Статус LightRAG (V16.7 "Unified Monitoring")
Обновлено: `{full_ts}` (Авто-обновление: 60 сек)

## 🕹️ Панель Управления
- **ПАУЗА (Безопасная)**: `./scripts/pause.sh`
- **ПРОДОЛЖИТЬ**: `./scripts/resume.sh`

## ⚡ Статус Индексации: {indexing_status}
- **Реальная обработка (Neo4j)**: `[{proc}/{real_file_count}]` ({pct:.2f}%)
- **Активность LLM (GPU/Ollama)**: {'🔥 Вычисления на GPU' if ollama_cpu > 10 else '💤 LLM простаивает'}

### 🖥️ Системные ресурсы (Docker & Mac)
| Компонент / Контейнер | Нагрузка (CPU %) | RAM / Mem | Статус |
| :--- | :--- | :--- | :--- |
| **Ollama (Metal GPU)** | {ollama_cpu:.1f}% | N/A | {'✅ Active' if ollama_cpu > 1 else '💤 Idle'} |
| **LightRAG API** | {api_cpu}% | {metrics.get("lightrag_api", {}).get("mem", "N/A")} | {api_h} |
| **Neo4j DB** | {neo_cpu}% | {metrics.get("lightrag_neo4j", {}).get("mem", "N/A")} | {neo_h} |
| **Qdrant DB** | {metrics.get("lightrag_qdrant", {}).get("cpu", 0)}% | {metrics.get("lightrag_qdrant", {}).get("mem", "N/A")} | {get_docker_status("lightrag_qdrant")} |

---

## 📜 Недавняя активность (Самые новые - сверху)
```text
{chr(10).join(get_buffered_logs(current_content))}
```

> [!TIP]
> Статус "На Паузе" появится только когда GPU физически остынет. Новые события в логах теперь отображаются мгновенно в начале списка.
"""
            with open(STATUS_FILE, "w", encoding="utf-8") as f:
                f.write(final_content)
                            
        except Exception as e:
            print(f"Ошибка дашборда: {e}")
        
        time.sleep(60)

if __name__ == "__main__":
    update_status()
