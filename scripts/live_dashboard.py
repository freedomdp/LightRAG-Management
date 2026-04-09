import os
import time
import json
import subprocess
from monitor_db import get_neo4j_stats, get_qdrant_stats

STATUS_FILE = "STATUS.md"
INGEST_STATUS_FILE = "temp/ingest_status.json"


def get_ingest_progress():
    if not os.path.exists(INGEST_STATUS_FILE):
        return None
    try:
        with open(INGEST_STATUS_FILE, "r") as f:
            return json.load(f)
    except:
        return None

def get_processing_progress():
    status_file = "rag_storage/kv_store_doc_status.json"
    if not os.path.exists(status_file):
        return None
    try:
        with open(status_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        total = len(data)
        processed = sum(1 for doc in data.values() if doc.get("status") == "processed")
        return {"processed": processed, "total": total}
    except:
        return None

def get_last_logs():
    try:
        # Пытаемся получить последние логи API
        result = subprocess.run(
            "docker logs --tail 25 lightrag_api", 
            shell=True, capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() or result.stderr.strip()
    except Exception as e:
        return f"Ошибка получения логов: {e}"

def get_ollama_status():
    try:
        # Проверяем нагрузку Ollama
        result = subprocess.run(
            "top -l 1 | grep ollama", 
            shell=True, capture_output=True, text=True, timeout=2
        )
        return "Активна (Обработка данных)" if result.stdout else "Ожидание"
    except:
        return "Неизвестно"

def generate_dashboard():
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    neo_stats = get_neo4j_stats()
    qdrant_stats = get_qdrant_stats()
    logs = get_last_logs()
    ollama = get_ollama_status()
    ingest = get_ingest_progress()
    proc = get_processing_progress()

    nodes = neo_stats.get("nodes", 0)
    rels = neo_stats.get("rels", 0)

    progress_section = ""
    # Ingestion Progress (Queueing)
    if ingest:
        current = ingest.get("current", 0)
        total = ingest.get("total", 0)
        percent = (current / total * 100) if total > 0 else 0
        last_file = ingest.get("last_file", "Нет")
        
        status_text = "✅ Завершено" if current == total else "🔄 В процессе"
        progress_section += f"""
## 🚀 Приемка файлов в очередь
- **Статус**: {status_text}
- **Прогресс**: `[{current}/{total}]` ({percent:.1f}%)
- **Последний файл**: `{last_file}`
"""

    # Processing Progress (Neo4j Indexing)
    if proc:
        p_current = proc.get("processed", 0)
        p_total = proc.get("total", 0)
        p_percent = (p_current / p_total * 100) if p_total > 0 else 0
        
        p_status = "✅ Готово" if p_current == p_total else "🧠 Обрабатывается LLM"
        progress_section += f"""
## 🧠 Реальная обработка (Neo4j)
- **Статус**: {p_status}
- **Прогресс**: `[{p_current}/{p_total}]` ({p_percent:.2f}%)
"""

    dashboard = f"""# 📊 Живой Статус LightRAG
Последнее обновление: `{timestamp}` (Обновляется каждые 30 сек)
{progress_section}
## 🗄️ Базы данных
| Метрика | Значение |
| :--- | :--- |
| **Узлы Neo4j (Сущности)** | {nodes} |
| **Связи Neo4j (Relationships)** | {rels} |
| **Статус Ollama** | {ollama} |

### 🧱 Векторные коллекции (Qdrant)
"""
    if isinstance(qdrant_stats, dict) and "error" not in qdrant_stats:
        for name, count in qdrant_stats.items():
            dashboard += f"- **{name}**: {count} точек\n"
    elif isinstance(qdrant_stats, dict) and "error" in qdrant_stats:
        dashboard += f"⚠️ {qdrant_stats.get('error')}\n"
    else:
        dashboard += f"⚠️ Коллекции не найдены или Qdrant отключен\n"

    dashboard += f"""
## 📜 Недавняя активность (Логи API)
```text
{logs}
```

---
> [!TIP]
> Держите этот файл открытым. Он обновляется автоматически.
"""
    
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        f.write(dashboard)

if __name__ == "__main__":
    while True:
        try:
            generate_dashboard()
        except Exception as e:
            # print(f"Error: {e}")
            pass
        time.sleep(30)
