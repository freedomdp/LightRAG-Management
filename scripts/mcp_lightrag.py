import asyncio
import httpx
import os
import json
from mcp.server.fastmcp import FastMCP

# Определение констант
LIGHTRAG_API_URL = "http://localhost:9621"
EXPERIENCE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "experience")

# Убедимся, что директория существует
os.makedirs(EXPERIENCE_DIR, exist_ok=True)

# Создаем MCP сервер
mcp = FastMCP("LightRAG_Assistant")

# Логирование для отладки

@mcp.tool()
async def query_knowledge(query: str, mode: str = "hybrid") -> str:
    """
    Поиск решения, концепции или фрагмента кода по базе знаний LightRAG.
    
    Args:
        query: Поисковый запрос или вопрос для системы.
        mode: Режим поиска (naive, local, global, hybrid). По умолчанию 'hybrid' - самый качественный.
    """
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                f"{LIGHTRAG_API_URL}/query",
                json={
                    "query": query,
                    "mode": mode,
                    "include_references": True
                }
            )
            response.raise_for_status()
            data = response.json()
            answer = data.get("response", "")
            references = data.get("references", [])
            
            # Фомируем понятный ответ
            result = f"🧠 Ответ от базы знаний:\n\n{answer}\n\n"
            if references:
                result += "📚 Источники:\n"
                for ref in references:
                    # Бывают как объекты, так и пути, учитываем оба варианта
                    if isinstance(ref, dict):
                        file_path = ref.get("file_path", "Неизвестно")
                        result += f"- {file_path}\n"
                    else:
                        result += f"- {ref}\n"
            return result
    except Exception as e:
        return f"Ошибка при обращении к LightRAG API: {str(e)}"

@mcp.tool()
async def check_project_standards(context: str) -> str:
    """
    Проверка кода или плана на соответствие текущим архитектурным стандартам и практикам проекта.
    
    Args:
        context: Описание вашей идеи, архитектурного решения или план действий. ИИ сверит это с базой.
    """
    prompt = f"Пользователь планирует следующее действие или решение:\n{context}\n\nОсновываясь на наших правилах проекта и стандартах архитектуры (описанных в project.md и файлах скиллов), содержит ли этот план ошибки или отклонения от курса? Как его следует реализовать правильно?"
    
    # Для концептуальных проверок лучше подходит global или hybrid
    return await query_knowledge(query=prompt, mode="hybrid")

@mcp.tool()
async def log_new_experience(title: str, content: str) -> str:
    """
    Сохранение нового опыта: конфигурационного решения, успешного скрипта или выявленной проблемы,
    чтобы база данных запомнила это на будущее.
    
    Args:
        title: Краткое название опыта (например, 'Интеграция n8n с OpenClaw').
        content: Подробное описание с примерами кода и выводами.
    """
    try:
        # Формируем md файл
        safe_title = "".join(c if c.isalnum() else "_" for c in title).strip("_").lower()
        file_path = os.path.join(EXPERIENCE_DIR, f"{safe_title}.md")
        
        md_content = f"# {title}\n\n{content}\n"
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        # Отправляем в API на немедленную индексацию
        async with httpx.AsyncClient(timeout=600.0) as client:
            response = await client.post(
                f"{LIGHTRAG_API_URL}/documents/text",
                json={
                    "text": md_content,
                    "description": f"New Experience: {title}"
                }
            )
            response.raise_for_status()
            
        return f"✅ Опыт успешно сохранен локально в {file_path} и отправлен на индексацию в базу!"
    except Exception as e:
        return f"Ошибка при сохранении опыта: {str(e)}"

@mcp.tool()
async def sync_tasks(action: str, task_text: str = None) -> str:
    """
    Управление файлом task.md проекта.
    
    Args:
        action: 'read' - прочитать задачи, 'add' - добавить задачу, 'toggle' - отметить как сделано/не сделано.
        task_text: Текст задачи (обязателен для add и toggle).
    """
    # Путь к task.md в корне проекта
    task_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "task.md")
    
    if not os.path.exists(task_file):
        with open(task_file, "w", encoding="utf-8") as f:
            f.write("# Список задач проекта\n\n")

    if action == "read":
        with open(task_file, "r", encoding="utf-8") as f:
            return f"📋 Текущие задачи:\n\n{f.read()}"

    elif action == "add":
        if not task_text:
            return "❌ Ошибка: task_text обязателен для добавления."
        with open(task_file, "a", encoding="utf-8") as f:
            f.write(f"- [ ] {task_text}\n")
        return f"✅ Задача добавлена: {task_text}"

    elif action == "toggle":
        if not task_text:
            return "❌ Ошибка: task_text нужен, чтобы найти задачу."
        
        with open(task_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        found = False
        new_lines = []
        for line in lines:
            if task_text in line and "- [" in line:
                if "[ ]" in line:
                    line = line.replace("[ ]", "[x]")
                    state = "выполнена"
                else:
                    line = line.replace("[x]", "[ ]")
                    state = "не выполнена"
                found = True
            new_lines.append(line)
        
        if found:
            with open(task_file, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            return f"✅ Статус задачи '{task_text}' изменен на '{state}'."
        else:
            return f"❌ Задача с текстом '{task_text}' не найдена."

    return "❌ Неизвестное действие (action)."

if __name__ == "__main__":
    # Запускаем MCP сервер через stdio
    mcp.run(transport='stdio')
