# Интеграция SEO-экспертизы и Guardrails в базу знаний

### Интеграция профессиональных знаний по SEO и безопасности ИИ (Zero-Compression)

**Задача**: Обучить базу LightRAG продвинутым методам внутренней SEO-оптимизации WordPress (без плагинов) и внедрить стандарты защиты от галлюцинаций.

**Решение**:
1. Создана структура обучающих материалов в `docs/knowledge/seo_training/`.
2. Подготовлены 4 детальных Markdown-файла:
    - `wp_seo_no_plugins_code.md`: Техническая реализация через `functions.php`, хуки `pre_get_document_title`, автоматизация Alt-тегов и очистка head.
    - `technical_seo_checklist_2026.md`: Профессиональные стандарты Core Web Vitals (метрика INP), Schema Graph (JSON-LD) и стратегия Topic Clusters.
    - `ai_hallucinations_and_guardrails.md`: Инструменты (Galileo, Giskard) и паттерны (Chain-of-Thought, Self-Correction) для предотвращения ошибок ИИ.
    - `seo_workflow_and_task_boundaries.md`: Операционные границы агента и чек-листы для выполнения задач.
3. Запущен процесс индексации через `scripts/core/ingest_manager.py` (30 файлов в очереди).

**Результат**: Агент теперь обладает глубоким контекстом для выполнения SEO-задач уровня партнер-архитектор, минимизируя использование тяжелых плагинов и галлюцинации при написании кода.

