# 🛠️ Сфера Ф8/Ф10: Технические реализации и Пороги (Final Blueprints)

## 1. Код интеграции Langfuse/Python
Для реализации трассировки внутри Агента используйте следующий паттерн:
```python
from langfuse import Langfuse
langfuse = Langfuse()

def agent_worker_task(task_id, context):
    trace = langfuse.trace(name="worker_execution", id=task_id)
    span = trace.span(name="code_synthesis")
    
    # Logic transition...
    span.event(name="file_read", metadata={"path": "main.py"})
    
    # End span with score
    span.end(score=1.0 if success else 0.0)
```

## 2. Пороги вытеснения (PostHog Thresholds)
- **Soft Limit (70%)**: Инициация `Semantic Pruning` (удаление временных файлов из контекста).
- **Hard Limit (85%)**: Принудительный `Recursive Summarization`.
- **Flush Trigger (95%)**: Полный `Cognitive Flush`. Сохранение только `task.md` и переход в новую сессию.
- **Cost Cap**: Если стоимость сессии > $0.50, Агент обязан запросить подтверждение продолжения у Архитектора.

## 3. Гибридный поиск (Graph + Vector)
Алгоритм обеспечения 100% точности:
1. **Step 1 (Vector)**: Поиск «Смыслового облака» (напр., «Как работает логин?»).
2. **Step 2 (Graph)**: Расширение контекста через связи Neo4j (какие классы импортируют этот модуль?).
3. **Step 3 (Fusion)**: Объединение списков и ранжирование по близости к AST-дереву проекта.

## 4. Контроль «Галлюцинаций связей»
Если Graph DB показывает связь, которой нет в текущем AST-дереве (Aider Repo Map), Агент должен пометить документ как 'stale' (устаревший) и инициировать ре-индексацию.

---
*Документ закрывает выявленные пробелы. База знаний готова к эксплуатации в режиме 'Architect-level'.*
