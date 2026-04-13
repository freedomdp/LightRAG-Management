# Antigravity Unified Core Expert System (HLV + SDD + ROI)

# Antigravity AI: Unified Core Expert System (HLV + SDD + Business ROI)

Этот документ является высшим техническим стандартом (Tier-1) для проекта Antigravity. Он объединяет методологии разработки (SDD/HLV) с фундаментальными бизнес-алгоритмами автономных систем.

## 🏗️ 1. Архитектурный цикл (SDD + HLV)
Разработка ведется строго по циклу Spec-Driven Development, где код — это производный артефакт спецификации:
1. Constitution: Мастер-стандарт проекта (project.md).
2. Specification: Описание логики ("Что" и "Почему").
3. Plan: Техническая декомпозиция (архитектура, API, данные).
4. Human Validation (HLV): Обязательная пауза для одобрения человеком ПЕРЕД реализацией.
5. Task Traceability: Выполнение через атомарные задачи в task.md.
6. Drift Guard: Запрещено изменять код без предварительного обновления спецификации и плана.

## 🧠 2. Анатомия Агента (Expert Stack)
На основе стандартов Lilian Weng и Huyen Chip:
- Planning (Brain): CoT/ToT, ReAct (Reason + Act), Self-Reflection (Reflexion).
- Memory (Dual-Layer Resilience): Short-term (Current context, handle Lost-in-the-Middle), Long-term (Vector DB, MIPS-algorithms like HNSW, ScaNN).
- Control Flows: Sequential, Parallel, For-Loop patterns instead of single prompts.

## 📈 3. Бизнес-логика и ROI (Strategic Alignment)
Focus on Value-at-Stake (HBR/Twilio):
- ROI Matrix: Automate only transactional tasks with clear success criteria.
- Identity Resolution: Deterministic Matching (100% accuracy via Email/ID) + Identity Graph (Merge Cookies/UserID/DeviceID). 4-Step IR Algorithm: Collect -> Match -> Merge -> Activate.

## 🚨 4. Эскалация и HITL (Handoff Protocol)
Anti-Dump Protocol:
- Triggers: Confidence < 0.7, Sentiment (Aggression), Scope violation.
- Structured Handover: Pass Structured State (Global Intent, Local Summary, Action Log) instead of chat logs.
- Graceful Handover: 30-sec parallel session active period.

## 🛡️ 5. Гвардейские стандарты (Hard Constraints)
- Zero-Compression Policy: Ingest technical docs without simplification.
- Fortress Protocol: Git + DB Backups before core changes.
- Audit-First: Every decision must reference an Expert Reference.

Статус: ДЕЙСТВУЮЩИЙ ЭТАЛОН.
