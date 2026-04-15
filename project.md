# 🗂️ LightRAG-Management: Конституция Проекта (v18.0 — HLV Era)

> **Единственный источник истины.** Все архитектурные решения, правила агента и стандарты проекта определяются здесь. Изменения только через HLV-цикл.

---

## 📖 Обзор

Проект направлен на создание универсального **Агента-Менеджера-Архитектора**, который подключается к любому рабочему проекту пользователя через MCP-протокол.

- **Ядро**: LightRAG (HKUDS) с FastAPI Wrapper — самообучающийся «центр мудрости».
- **Миссия**: Исключить повторение ошибок в любой точке экосистемы. Агент — не кодер, а **партнёр-архитектор**.
- **Бизнес-контекст**: Фундамент для агентства по продаже ИИ-решений (сайты + автоматизация для малого бизнеса).

---

## 🛠️ Технологический Стек

| Слой | Технология | Назначение |
|---|---|---|
| **LLM** | Gemma 4 (`gemma4:e4b`) via Ollama / Metal GPU | Локальный языковой движок |
| **Embedding** | `nomic-embed-text` via Ollama | Векторизация |
| **RAG Движок** | LightRAG (FastAPI Wrapper) | Долгосрочная память и граф знаний |
| **Graph DB** | Neo4j | Хранение сущностей и связей |
| **Vector DB** | Qdrant | Хранение эмбеддингов |
| **MCP** | `scripts/mcp_lightrag.py` | Протокол связи Antigravity ↔ LightRAG |
| **Оркестрация** | n8n (Docker) | Workflow-автоматизация, Telegram-бот |
| **Инфраструктура** | Docker Compose | Контейнеризация всех сервисов |
| **Источник знаний** | NotebookLM (Gemini 2.5) | Первичный источник для JIT-индексации |

---

## 📂 Структура Проекта (HLV-Standard)

```
LightRAG/
├── project.md              # ← КОНСТИТУЦИЯ (этот файл, Tier-1)
├── STATUS.md               # Живая панель мониторинга (авто-обновление)
├── task.md                 # Текущий HLV-Board задач
├── RULES.md                # Короткие операционные правила для быстрого доступа
├── docker-compose.yml      # Инфраструктура
├── .env                    # Секреты и конфигурация (не в Git)
│
├── scripts/
│   ├── core/               # Основные движки системы
│   │   ├── ingest_manager.py     # Пошаговая загрузка данных
│   │   ├── chat.py               # Интерактивный чат с базой
│   │   └── dashboard_engine.py   # Движок живого дашборда
│   ├── utils/              # Вспомогательные утилиты
│   │   ├── backup_manager.py     # Резервное копирование
│   │   ├── monitor_db.py         # Мониторинг состояния БД
│   │   ├── pdf_to_md.py          # Конвертация PDF
│   │   ├── split_heavy_docs.py   # Разбивка тяжёлых документов
│   │   └── surgical_purge.py     # Точечная очистка по ID
│   ├── mcp_lightrag.py     # MCP-сервер (точка входа для Antigravity)
│   └── archive/            # Устаревшие скрипты (не использовать)
│
├── docs/
│   ├── knowledge/          # База знаний для индексации (источник правды для RAG)
│   │   └── new_ingest/     # Очередь на индексацию
│   ├── experience/         # Lessons Learned (авто-генерация через log_new_experience)
│   └── architecture.md     # Диаграммы и детальное описание архитектуры
│
├── rag_storage/            # Индексы LightRAG (НЕ трогать вручную)
├── neo4j_data/             # Данные Neo4j (НЕ трогать вручную)
├── qdrant_data/            # Данные Qdrant (НЕ трогать вручную)
├── backups/                # Архивы бэкапов (backup_YYYYMMDD_HHMMSS.zip)
└── temp/                   # Временные данные, логи (в .gitignore)
```

---

## 🏗️ Архитектурный Цикл (SDD + HLV)

Все изменения в системе проходят через обязательный цикл:

```
Constitution (project.md)
    ↓
[SPECIFICATION] — Что делаем и Почему
    ↓
[PLANNING] — Техническая декомпозиция (файлы, API, данные)
    ↓
[VALIDATION] ← Human Approval ← ОБЯЗАТЕЛЬНАЯ ОСТАНОВКА
    ↓
[EXECUTION] — Атомарные задачи в task.md
    ↓
[VERIFICATION] — Тесты, query_knowledge, check_project_standards
    ↓
[LEARNING] — log_new_experience + Git Commit
```

> **Drift Guard**: Код не меняется без предварительного обновления спецификации. Нарушение → откат по Git.

---

## 🧠 11 Функций Агента-Менеджера

1. **Контроль ТЗ**: Непрерывная сверка действий с техническим заданием.
2. **Task Management**: Ведение HLV-Board в `task.md` (статусы: SPECIFICATION / PLANNING / VALIDATION / EXECUTION / VERIFICATION).
3. **Сохранение Фокуса**: Одна задача за итерацию. Предотвращение «размытия».
4. **Архитектурный Надзор**: Изменения — только через план. HLV + Осознанный вайб-кодинг (Манифест 1.8).
5. **VibeContract**: Описание Pre/Post-conditions ПЕРЕД генерацией логики.
6. **Управление Скиллами**: JIT-проксирование (схемы в промпте, код — по запросу).
7. **Анализ Ошибок**: Фиксация Lessons Learned → `log_new_experience`.
8. **Постоянное Самообучение**: Мониторинг прогресса, успешных решений через LightRAG.
9. **Субъектность**: Управление через архитектурный уровень. Ноль галлюцинаций.
10. **Checkpoint Management**: Git commits + DB backups перед любыми крупными операциями.
11. **ROI-Gate**: Автоматизация проходит проверку на транзакционную ценность (Build/Buy/Wait).

### 🚫 Железное Правило (The Iron Rule)
**Агенту ЗАПРЕЩЕНО** изучать исходный код напрямую или изменять `project.md`, `.env`, `docker-compose.yml` методом полного затирания. Только точечные правки (append / replace lines).

---

## 🏗️ Анатомия Агента (Expert Stack)

На основе стандартов Lilian Weng и Chip Huyen:

- **Planning (Brain)**:
    - **ReAct**: Замкнутый цикл «Рассуждение + Действие».
    - **Self-Reflection (Reflexion)**: Критика и исправление прошлых шагов.
- **Memory (Dual-Layer)**:
    - **Short-term**: Эффективное использование контекстного окна (Lost-in-the-Middle aware).
    - **Long-term**: Vector DB (Qdrant) + Graph DB (Neo4j) с HNSW-поиском.
- **Control Flows**: Programmatic patterns (Sequential, Parallel, For-Loop) вместо одного промпта.

---

## 📈 Бизнес-логика и Anti-Hallucination Stack

### ROI Matrix
- Автоматизация только транзакционных задач с чётким критерием успеха.
- Матрица: Build (ROI > 3x за 6 мес.) / Buy (SaaS) / Wait (зрелость < 80%).

### Anti-Freeze Watcher (n8n)
- **Таймаут**: 15-20 сек. на ответ ИИ. Параллельный узел-сторож.
- **Fallback**: «Обрабатываю сложный запрос, подключаю специалиста.»
- **Alert**: Менеджер в Slack/CRM получает Structured State (Intent + Summary + Actions).

### Structured Handoff (Anti-Dump Protocol)
- **Triggers**: Confidence < 0.7 / Sentiment-Alert / выход за Scope.
- **Запрещён**: Context Dump (лог переписки). Только Structured State.
- **Graceful Handover**: 30 сек. параллельной активности при передаче.

### Identity Resolution (Omnichannel)
- **Identity Graph**: Маппинг TG_ID / WhatsApp / Email → CRM_ID (Postgres/HubSpot).
- **Matching**: Детерминированный (100% точность по Email/Phone) → Probabilistic.
- **Algorithm**: Collect → Match → Merge → Activate.

---

## 🔐 Стандарты целостности данных (Data Integrity Standards)

1. **Запрет на жесткое отключение**: Разрешена только «мягкая» остановка через `docker compose stop`. Категорически запрещено использование `docker kill` или `down -v` без предварительного подтверждения наличия свежего бэкапа.
2. **Pre-Ingest Snapshot**: Перед началом индексации более 1 документа система ОБЯЗАНА создать автоматический снимок папки `rag_storage` через `backup_manager.py`.
3. **Startup Integrity Guard**: При каждом старте системы или перед выполнением критических запросов агент обязан выполнить проверку целостности всех JSON-хранилищ (`verify_integrity`).
4. **Хранение логов экстракции**: Любые ошибки декодирования или повреждения файлов должны немедленно фиксироваться в `STATUS.md` с блокировкой дальнейших операций до ручного вмешательства.

---

## 🛡️ Гвардейские Стандарты (Hard Constraints)

| Правило | Детали |
|---|---|
| **ANTI-OVERWRITE** | Запрещено полное затирание конфиг-файлов. Только append/replace. |
| **FORTRESS PROTOCOL** | Бэкап (`backups/`) обязателен перед индексацией > 5 доков и любой очисткой. |
| **SURGICAL PURGE ONLY** | Удаление данных — только через API по конкретным ID. Не `rm -rf`. |
| **ZERO-COMPRESSION** | Техническая документация в базе — без упрощений (алгоритмы, формулы). |
| **AUDIT-FIRST** | Каждое решение имеет ссылку на проверенный источник. |
| **JIT INGEST** | Запрещён batch dump. Индексация — только под конкретную активную задачу. |
| **RUSSIAN ONLY** | Все ответы агента и документация — строго на русском языке. |

---

## 🚦 Fortress Protocol Checklist
*Обязательная проверка перед запуском системы или индексации.*

### Уровень 1: Инфраструктура
- [ ] `docker ps` — статус `Up` и `Healthy` для LightRAG API, Neo4j, Qdrant.
- [ ] Порты: `9621` (API), `7474` (Neo4j), `6333` (Qdrant) доступны.

### Уровень 2: Модели
- [ ] `ollama list` содержит `gemma4:e4b` и `nomic-embed-text`.
- [ ] `ollama ps` — только нужные модели загружены.

### Уровень 3: Данные (Integrity)
- [ ] `backup_manager.py --verify` — все JSON-хранилища валидны (нет ошибок декодирования).
- [ ] Neo4j: `MATCH (n) RETURN count(n)` → ожидается 14,775+ узлов.
- [ ] Qdrant: Коллекции активны (проверить через логи или UI).
- [ ] RAG Storage: Наличие файлов `kv_store_*.json` в `rag_storage/`.

### Уровень 4: Конфигурация
- [ ] `.env`: `LLM_MODEL=gemma4:e4b`, `EMBEDDING_MODEL=nomic-embed-text`.
- [ ] `MAX_PARALLEL_INSERT=1` во избежание перегрева.

### Уровень 5: Безопасность
- [x] Свежий бэкап в `backups/` перед началом работ.
- [x] Git checkpoint зафиксирован.

---

## 📚 Ключевые Ресурсы

- **NotebookLM (Основной)**: [AI Автоматизация / LightRAG Management](https://notebooklm.google.com/notebook/b3977ee0-e50b-4d9a-a7e3-2d3deb9c1cef)
- **LightRAG API**: `http://localhost:9621`
- **Neo4j Browser**: `http://localhost:7474`
- **Qdrant UI**: `http://localhost:6333/dashboard`
- **[📊 ЖИВОЙ СТАТУС](file:///Users/sergej/StudioProjects/LightRAG/STATUS.md)**

---

## 🏁 Прогресс Проекта

- [x] Инфраструктура Docker (Neo4j + Qdrant + LightRAG API).
- [x] MCP-сервер (`scripts/mcp_lightrag.py`) активен.
- [x] JIT Agentic Ingestion Protocol (Variant 1) утверждён.
- [x] Core Expert System (HLV + SDD + ROI) формализован и проиндексирован.
- [x] Осознанный вайб-кодинг (Манифест 1.8) внедрён.
- [x] Zero-Compression обучение по 10+ техническим материалам (Weng, Chip, HBR, Twilio).
- [x] Архитектура Anti-Freeze, Omnichannel IR, Guardrails задокументирована и проиндексирована.
- [x] **v18.0**: Реструктуризация под HLV/SDD. Единая Конституция. Чистая структура.
