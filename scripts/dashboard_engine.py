import os
import json
import time
import subprocess
import datetime
import glob

STATE_FILE = "/Users/sergej/StudioProjects/LightRAG/temp/dashboard_state.json"
STATUS_FILE = "/Users/sergej/StudioProjects/LightRAG/STATUS.md"
TMP_STATUS = "/Users/sergej/StudioProjects/LightRAG/temp/STATUS.md.tmp"
LOGS_MAX_LINES = 100

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    except Exception:
        return ""

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {"events": []}
    return {"events": []}

def save_state(state):
    os.makedirs("/Users/sergej/StudioProjects/LightRAG/temp", exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def log_event(state, msg):
    ts = datetime.datetime.now().strftime("[%H:%M:%S]")
    state["events"].insert(0, f"{ts} {msg}")
    state["events"] = state["events"][:LOGS_MAX_LINES]
    save_state(state)

def get_doc_counts():
    # Находим все физические файлы в папке docs
    files_on_disk = glob.glob("/Users/sergej/StudioProjects/LightRAG/docs/**/*.md", recursive=True)
    total_files = len(files_on_disk)
    
    # Извлекаем только базовые имена файлов для сопоставления
    basenames_on_disk = {os.path.basename(f) for f in files_on_disk}
    
    doc_status = {}
    if os.path.exists("/Users/sergej/StudioProjects/LightRAG/rag_storage/kv_store_doc_status.json"):
        with open("/Users/sergej/StudioProjects/LightRAG/rag_storage/kv_store_doc_status.json", "r") as f:
            try:
                doc_status = json.load(f)
            except Exception:
                pass
    
    processed_count = 0
    pending_count = 0
    indexed_basenames = set()
    
    # Проверяем статус только для тех файлов, которые есть на диске
    for doc_id, info in doc_status.items():
        fname = info.get("file_path") or ""
        base = os.path.basename(fname)
        if fname in basenames_on_disk or base in basenames_on_disk:
            status = info.get("status")
            if status in ["processed", "success"]:
                processed_count += 1
                indexed_basenames.add(base)
            elif status in ["pending", "processing", "extracting", "creating"]:
                pending_count += 1
                indexed_basenames.add(base)
                
    # Файлы, которых нет в базе RAG (совсем не начаты)
    unindexed_count = total_files - len(indexed_basenames)
    if unindexed_count < 0: unindexed_count = 0
        
    return processed_count, total_files, pending_count, unindexed_count

def get_docker_stats():
    out = run_cmd('/usr/local/bin/docker stats --no-stream --format "{{.Name}}:{{.CPUPerc}}:{{.MemUsage}}"')
    stats = {}
    for line in out.splitlines():
        parts = line.split(":")
        if len(parts) >= 3:
            stats[parts[0]] = {"cpu": parts[1], "mem": parts[2]}
    return stats

def get_ollama_stats():
    out = run_cmd("ps -A -o %cpu,command | grep ollama | grep -v grep")
    total_cpu = 0.0
    for line in out.splitlines():
        parts = line.strip().split()
        if parts:
            try:
                total_cpu += float(parts[0])
            except Exception:
                pass
    return f"{total_cpu:.1f}%"

def check_lightrag_logs(state):
    logs = run_cmd("/usr/local/bin/docker logs --tail 50 lightrag_api 2>&1")
    if "ERROR" in logs.upper() or "TIMEOUT" in logs.upper():
        pass

last_processed = -1
state = load_state()
log_event(state, "▶️ Запуск скрипта индексации дашборда V3.1")

while True:
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    proc, total, pending, unindexed = get_doc_counts()
    
    if proc != last_processed and last_processed != -1:
        diff = proc - last_processed
        if diff > 0:
            log_event(state, f"📄 Документ обработан (графы построены): +{diff} файлов.")
            
    check_lightrag_logs(state)
    
    last_processed = proc
    
    docker_stats = get_docker_stats()
    oll_cpu = get_ollama_stats()
    
    try:
        oll_val = float(oll_cpu.replace('%',''))
        oll_load = "✅ Активна" if oll_val > 1.0 else "💤 LLM простаивает"
    except Exception:
        oll_load = "⚠️ Ошибка парсинга"

    api_stat = docker_stats.get("lightrag_api", {"cpu":"0%", "mem":"0"})
    neo_stat = docker_stats.get("lightrag_neo4j", {"cpu":"0%", "mem":"0"})
    qd_stat = docker_stats.get("lightrag_qdrant", {"cpu":"0%", "mem":"0"})
    
    try:
        api_val = float(api_stat['cpu'].replace('%',''))
        api_load = "⚠️ High Load" if api_val > 80 else "✅ Online"
    except Exception:
        api_load = "✅ Online"
    
    progress_pct = (proc / total * 100) if total > 0 else 0
    sys_status = "Индексация" if (pending > 0 or unindexed > 0) else ("Покой" if total > 0 else "Пусто")

    md = f"""# Спецификация и Правила Формирования Дашборда (STATUS.md) V3.1
Обновлено: {now_str} (Авто-обновление: 60 сек)

## ⚡ Статус Индексации
- **Общий статус системы**: {sys_status}
- **Реальная обработка (Batch Progress)**: [{proc}/{total}] ({progress_pct:.1f}%)
- **Статусы файлов**:
    - ✅ Проиндексировано: {proc}
    - ⏳ В работе (Ollama): {pending}
    - 🛑 Не начато (Вне базы): {unindexed}
- **Активность LLM (GPU/Ollama)**: {oll_load}

## 🖥️ Системные ресурсы (Docker & Mac)
| Компонент / Контейнер | Нагрузка (CPU %) | RAM / Mem | Статус |
| :--- | :--- | :--- | :--- |
| Ollama (Metal GPU) | {oll_cpu} | - | {oll_load} |
| LightRAG API (`lightrag_api`) | {api_stat['cpu']} | {api_stat['mem']} | {api_load} |
| Neo4j DB (`lightrag_neo4j`) | {neo_stat['cpu']} | {neo_stat['mem']} | ✅ Online |
| Qdrant DB (`lightrag_qdrant`) | {qd_stat['cpu']} | {qd_stat['mem']} | ✅ Online |

## 📜 Недавняя активность (Самые новые - сверху)
"""
    for ev in state["events"]:
        md += f"- {ev}\n"
    
    os.makedirs("/Users/sergej/StudioProjects/LightRAG/temp", exist_ok=True)
    with open(TMP_STATUS, "w", encoding="utf-8") as f:
        f.write(md)
        
    os.rename(TMP_STATUS, STATUS_FILE)
    
    time.sleep(60)

