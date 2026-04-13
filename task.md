# 📋 HLV-Board: Активные Задачи

> **Цикл**: Specification → Planning → [Human Validation] → Execution → Verification → Learning

---

## 🟢 [COMPLETED] Реструктуризация проекта под HLV/SDD v18.0

**Спецификация**: Привести проект к полному соответствию методологии HLV/SDD — единая Конституция, чистая архитектура папок, рабочий процесс со строгими чекпоинтами.

**Validation**: ✅ Одобрено пользователем 2026-04-14 01:57

**Выполнено**:
- [x] Создана единая Конституция `project.md` (v18.0)
- [x] Удалены дубликаты `docs/project.md`, `docs/STATUS.md`
- [x] `scripts/` реорганизован: `core/` + `utils/` + `archive/`
- [x] Удалены `.broken`, `.corrupt`, `.log` файлы
- [x] Обновлён `.gitignore` (comprehensive rules)
- [x] Git commit зафиксирован

---

## 🔵 [SPECIFICATION] Следующий шаг: Первый ИИ-Агент для Бизнеса

**Идея**: Собрать первый production-ready ИИ-агент на базе n8n для одной из проработанных ниш (Anti-Freeze + Omnichannel + Handoff).

**Кандидаты на первый кейс**:
- [ ] Кондиционеры: Pre-diagnostic агент (мультимодальный)
- [ ] Салон красоты/маникюр: Retention & Reputation Engine
- [ ] Универсальный: Lead Capture бот для агентства (для себя)

---

## 📐 Как использовать этот файл

```
## [SPECIFICATION] Название задачи — Что и Почему
## [PLANNING] Декомпозиция — файлы, API, данные
## [VALIDATION] ← Ждём Human Approval перед началом
## [EXECUTION] — [ ] Атомарные шаги кода
## [VERIFICATION] — Как проверяем результат
## [LEARNING] — log_new_experience + Git commit
```
