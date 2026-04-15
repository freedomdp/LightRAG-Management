# HLV Project Board: AI Agency Market Intelligence

## Phase 1: Specification & Planning [COMPLETED]
- [x] Определение бизнес-модели M.O.N.E.Y. v2.0
- [x] Согласование лимита в 100 отзывов и аудита репутации
- [x] План реализации v2.1 утвержден (логика сбора и анализа)

## Phase 2: Mapping Engine (Data Acquisition) [/]
- [ ] Исследование API Outscraper для выгрузки 100 отзывов + ответов бизнеса
- [ ] Разработка `scripts/core/mapping_engine.py` (Сборщик данных)
- [ ] Тестирование сбора данных на 3 тестовых компаниях

## Phase 3: Pain & Reputation Analysis [/]
- [ ] Создание промптов для `pain_analyser.py` (Анализ 100 отзывов + Работа с негативом)
- [ ] Генерация JSON-профиля компании (Lead DNA)
- [ ] Подготовка текста для 1-го письма на основе реальных "болей" и "пробелов в ответах"

## Phase 4: Verification & Pre-Outreach [ ]
- [ ] Валидация точности анализа через HLV (Human validation)
- [ ] Генерация пробного письма и структуры лендинга
- [ ] Подготовка к интеграции с WordPress (в будущем)

---
*Статус: Готов к разработке `mapping_engine.py`.*
- [ ] Подготовка ТЗ для n8n ворклоу (M.O.N.E.Y. Engine) - В РАБОТЕ (Ждет фидбека)
- [ ] Проработка гибридной архитектуры Agency-Base (SQLite + LightRAG) - ЖДЕТ РЕШЕНИЯ
