import asyncio
import httpx
import os
import sys
import json
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

# Загрузка настроек из .env
load_dotenv()

# Конфигурация
LIGHTRAG_API_URL = os.getenv("LIGHTRAG_API_URL", "http://localhost:9621")
EXPERIENCE_DIR = os.getenv("EXPERIENCE_DIR", "./docs/experience")
TASK_FILE = os.getenv("TASK_FILE", "./task.md")
LOG_FILE = os.getenv("LOG_FILE", "./mcp_server.log")

# Настройка логирования в stderr, чтобы не мешать протоколу stdio
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("mcp_lightrag")

# Создаем MCP сервер
mcp = FastMCP("LightRAG_PRO")

class LightRAGClient:
    """Удобный клиент для взаимодействия с API LightRAG."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.timeout = httpx.Timeout(300.0, connect=10.0)

    async def fetch(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Универсальный метод для HTTP запросов."""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Вызов API: {method} {url}")
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.request(method, url, **kwargs)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"Ошибка API ({e.response.status_code}): {e.response.text}")
                raise Exception(f"API вернул ошибку {e.response.status_code}: {e.response.text}")
            except Exception as e:
                logger.error(f"Ошибка сетевого соединения: {str(e)}")
                raise Exception(f"Не удалось связаться с LightRAG: {str(e)}")

client = LightRAGClient(LIGHTRAG_API_URL)

# --- Группа "ЗНАНИЯ И ПОИСК" ---

@mcp.tool()
async def query_knowledge(query: str, mode: str = "hybrid") -> str:
    """
    Поиск ответа в базе знаний LightRAG.
    
    Args:
        query: Ваш вопрос или поисковый запрос (на русском).
        mode: naive (простой), local (локальный граф), global (глобальный граф), hybrid (комбинация всех).
    """
    try:
        data = await client.fetch("POST", "/query", json={"query": query, "mode": mode, "include_references": True})
        answer = data.get("response", "Ответ не получен.")
        references = data.get("references", [])
        
        result = f"🧠 Ответ от LightRAG ({mode}):\n\n{answer}\n\n"
        if references:
            result += "📚 Источники:\n"
            for ref in references:
                path = ref.get("file_path", ref) if isinstance(ref, dict) else ref
                result += f"- {path}\n"
        return result
    except Exception as e:
        return f"❌ Ошибка поиска: {str(e)}"

@mcp.tool()
async def query_data(query: str) -> str:
    """
    Получение сырых данных из графа знаний (объекты, отношения).
    """
    try:
        data = await client.fetch("POST", "/query/data", json={"query": query})
        return f"📊 Данные графа:\n\n{json.dumps(data, indent=2, ensure_ascii=False)}"
    except Exception as e:
        return f"❌ Ошибка выгрузки данных: {str(e)}"

# --- Группа "ОБУЧЕНИЕ (ИНДЕКСАЦИЯ)" ---

@mcp.tool()
async def ingest_text(text: str, description: str = "Manual Ingest") -> str:
    """
    Обучение базы: отправить произвольный текст на индексацию.
    """
    try:
        await client.fetch("POST", "/documents/text", json={"text": text, "description": description})
        return f"✅ Текст успешно отправлен на обучение. Описание: {description}"
    except Exception as e:
        return f"❌ Ошибка индексации текста: {str(e)}"

@mcp.tool()
async def ingest_file(file_path: str) -> str:
    """
    Обучение базы: отправить локальный файл на индексацию (нужен полный путь).
    """
    try:
        if not os.path.exists(file_path):
            return f"❌ Ошибка: Файл {file_path} не найден."
            
        with open(file_path, 'rb') as f:
            files = {'file': f}
            async with httpx.AsyncClient(timeout=600.0) as async_client:
                response = await async_client.post(f"{LIGHTRAG_API_URL}/documents/upload", files=files)
                response.raise_for_status()
                
        return f"✅ Файл {os.path.basename(file_path)} успешно загружен и отправлен на обучение."
    except Exception as e:
        return f"❌ Ошибка загрузки файла: {str(e)}"

# --- Группа "УПРАВЛЕНИЕ БАЗОЙ" ---

@mcp.tool()
async def get_status() -> str:
    """
    Проверка здоровья системы и статистика базы знаний (кол-во сущностей, документов и т.д.).
    """
    try:
        health = await client.fetch("GET", "/health")
        counts = await client.fetch("GET", "/documents/status_counts")
        
        status_msg = f"🛰 Статус LightRAG API: {health.get('status', 'Unknown')}\n"
        status_msg += f"📦 Статистика документов:\n"
        for key, val in counts.items():
            status_msg += f"- {key}: {val}\n"
            
        return status_msg
    except Exception as e:
        return f"❌ Ошибка получения статуса: {str(e)}"

@mcp.tool()
async def list_documents(limit: int = 20) -> str:
    """
    Показать список последних проиндексированных документов.
    """
    try:
        # Пытаемся получить список документов (эндпоинт может отличаться в разных версиях)
        data = await client.fetch("GET", f"/documents/paginated?limit={limit}")
        docs = data.get("documents", [])
        
        if not docs:
            return "📭 База знаний пока пуста."
            
        result = f"📄 Список последних документов ({len(docs)}):\n"
        for doc in docs:
            name = doc.get("file_path", "Unknown")
            status = doc.get("status", "unknown")
            created = doc.get("created_at", "")[:19].replace("T", " ")
            result += f"- [{status}] {name} ({created})\n"
        return result
    except Exception as e:
        return f"❌ Ошибка при получении списка: {str(e)}"

@mcp.tool()
async def delete_document(doc_id_or_path: str) -> str:
    """
    Удалить выбранный документ из базы знаний.
    """
    try:
        await client.fetch("POST", "/documents/delete_document", json={"doc_id": doc_id_or_path})
        return f"🗑 Документ '{doc_id_or_path}' успешно удален из базы."
    except Exception as e:
        # Попробуем удалить как путь, если ID не сработал
        return f"❌ Ошибка удаления: {str(e)}"

# --- Группа "РАБОЧИЙ ПРОЦЕСС" ---

@mcp.tool()
async def log_new_experience(title: str, content: str) -> str:
    """
    Сохранение нового опыта в файл .md и его автоматическая индексация в базу.
    """
    try:
        os.makedirs(EXPERIENCE_DIR, exist_ok=True)
        safe_title = "".join(c if c.isalnum() else "_" for c in title).strip("_").lower()
        file_name = f"{safe_title}.md"
        full_path = os.path.join(EXPERIENCE_DIR, file_name)
        
        md_content = f"# {title}\n\n{content}\n\n*Зафиксировано: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        # Сразу отправляем на индексацию
        await ingest_text(text=md_content, description=f"New Experience: {title}")
        
        return f"✅ Опыт зафиксирован в файле {file_name} и отправлен в базу знаний."
    except Exception as e:
        return f"❌ Ошибка при фиксации опыта: {str(e)}"

@mcp.tool()
async def sync_tasks(action: str, task_text: str = None) -> str:
    """
    Управление файлом задач task.md (read, add, toggle).
    """
    try:
        if action == "read":
            if not os.path.exists(TASK_FILE):
                return "📭 Список задач пока пуст."
            with open(TASK_FILE, "r", encoding="utf-8") as f:
                return f"📋 Список задач:\n\n{f.read()}"
        
        elif action == "add":
            if not task_text: return "❌ Укажите текст задачи."
            with open(TASK_FILE, "a", encoding="utf-8") as f:
                f.write(f"- [ ] {task_text}\n")
            return f"✅ Задача добавлена: {task_text}"
            
        elif action == "toggle":
            if not task_text: return "❌ Укажите текст задачи для поиска."
            if not os.path.exists(TASK_FILE): return "❌ Файл task.md не найден."
            
            with open(TASK_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            new_lines = []
            found = False
            for line in lines:
                if task_text in line:
                    if "[ ]" in line:
                        line = line.replace("[ ]", "[x]")
                        found = True
                    elif "[x]" in line:
                        line = line.replace("[x]", "[ ]")
                        found = True
                new_lines.append(line)
            
            if found:
                with open(TASK_FILE, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                return f"✅ Статус задачи '{task_text}' изменен."
            return "❌ Задача не найдена."
            
        return "❌ Неизвестное действие. Используйте: read, add, toggle."
    except Exception as e:
        return f"❌ Ошибка управления задачами: {str(e)}"

if __name__ == "__main__":
    # Запуск сервера через stdio transport
    mcp.run(transport='stdio')
