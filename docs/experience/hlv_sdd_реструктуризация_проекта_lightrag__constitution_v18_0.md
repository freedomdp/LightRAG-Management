# HLV/SDD Реструктуризация проекта LightRAG (Constitution v18.0)

### Задача
Перевести проект LightRAG-Management на полный цикл HLV (Human-LLM-Validation) и SDD (Spec-Driven Development). Навести порядок в структуре и создать основу для масштабирования бизнеса.

### Что было сделано (Фазы выполнения)

**Фаза 1 (Fortress Protocol):** Перед началом создан бэкап `backup_20260414_014933.zip` и сделан Git checkpoint.

**Фаза 2 (Единая Конституция):**
- `project.md` в корне переписан как единственный источник правды (Tier-1). Включает: стек, структуру, 11 функций агента, HLV-цикл, Anti-Freeze/Omnichannel/Guardrails архитектуры, Fortress Checklist.
- Удалены дубликаты `docs/project.md` и `docs/STATUS.md`.

**Фаза 3 (Реорганизация scripts/):**
- `scripts/core/` — основные движки: `ingest_manager.py`, `chat.py`, `dashboard_engine.py`.
- `scripts/utils/` — утилиты: `backup_manager.py`, `monitor_db.py`, `pdf_to_md.py`, `split_heavy_docs.py`, `surgical_purge.py`, `init_status.py`, `agent_brain.py`, `sync_notebooklm.py`, `test_gemma_knowledge.py`.
- Точка входа MCP осталась на уровне `scripts/mcp_lightrag.py`.

**Фаза 4 (Гигиена данных):**
- Удалены: `rag_storage/*.broken`, `rag_storage/*.corrupt`, `temp/*.log`, `scripts/__pycache__`, логи `scripts/`.

**Фаза 5 (task.md):**
- `task.md` переведён в HLV-Board формат: Specification → Planning → Validation → Execution → Verification → Learning.

**Фаза 6 (.gitignore):**
- Добавлены правила: `*.log`, `*.broken`, `*.corrupt`, `*.bak`, `**/__pycache__/`, `scripts/ingest_status.json`.

### Рекомендации базы знаний (Strangler Fig Pattern)
LightRAG подтвердил правильность направления и рекомендовал при дальнейшем рефакторинге Python-логики использовать Strangler Fig Pattern — постепенную замену старых функций новыми без риска регрессии.

### Затронутые файлы
- `project.md` (полная перезапись)
- `task.md` (HLV-Board формат)
- `.gitignore` (усилен)
- `scripts/core/` [NEW], `scripts/utils/` [NEW]
- `docs/project.md`, `docs/STATUS.md` [DELETED]
- `rag_storage/*.broken/.corrupt`, `temp/*.log` [DELETED]

[Tags: HLV, SDD, project-structure, refactoring, Constitution-v18, scripts-core, strangler-fig]
