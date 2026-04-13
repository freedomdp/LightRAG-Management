# HLV Architecture Expert Guide (Human-LLM-Validation)

# Архитектура HLV (Human-LLM-Validation): Глубокий стандарт разработки

Архитектура HLV — это система «Контрактного программирования для ИИ», устраняющая недетерминированность LLM-агентов.

## 1. Трехслойная структура (The Three Layers)
### 🔵 Слой Человека (Human Layer - "The What")
Источник истины (Source of Truth):
- Glossary (glossary.yaml): Бизнес-объекты (JSON Schema).
- Contracts (contracts/*.yaml): Формальные спецификации функций.
- Constraints (constraints/): Ограничения (security, perf, arch).
- Map (map.yaml): Индекс всех файлов проекта.

### 🟢 Слой LLM (LLM Layer - "The How")
Реализация логики:
- Implementation: Код (Rust, Python, JS).
- Tracing: Маркеры в коде для связи с контрактами.

### 🔴 Слой Валидации (Validation Layer - "The Guard")
Автоматический контроль (CLI hlv):
- Checkers: Скрипты проверки соответствия контрактам.
- Gates: Блокирующие условия завершения задачи.

## 2. Техническая реализация (Deep Specs)
### 🏗️ Система Маркеров (Traceability Markers)
Синтаксис: // @hlv <CONTRACT_ID> или # @hlv <CONTRACT_ID>.
Пример: // @hlv INVALID_PASSWORD.
Валидация: hlv check парсит код и выявляет отсутствие маркеров для контрактных условий.

### 🧱 Контракты (Contracts)
Состав: inputs_schema, outputs_schema, errors (с полем when), invariants.

### 🚪 Гейты (Gates Policy)
Описание в validation/gates-policy.yaml. Каждая команда должна вернуть успех.
Примеры: contract_coverage (hlv check --markers), security_audit (hlv scan-security).

## 3. Сравнение: AI Factory vs HLV
- AI Factory: Массовая генерация (Quantity).
- HLV Architecture: Инженерное качество (Quality), сложные системы, нулевой риск (блокировка ошибок валидатором).

## 🚀 Workflow
1. Инициализация (hlv init).
2. Артефакты (contracts, glossary).
3. Индексация (map.yaml).
4. Кодинг (implementation + markers).
5. Верификация (hlv check). Провал гейтов -> возврат к шагу 4.

Архитектура HLV — это «спасательный круг» для Vibe Coding.
