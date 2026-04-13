# Human-in-the-Loop (HITL) & Handoff Patterns

# Проектирование Handoff и Human-in-the-Loop (Expert-Level)

Стандарт определяет алгоритмы эскалации и передачи контекста, минимизируя "Context Breakdown".

## 🚨 Многоуровневые триггеры эскалации
1. Уровень Намерений (Intent-Based): Direct Request ("оператор"), Scope Violation (Zero-shot classification).
2. Уровень Эмоций (Sentiment-Based): Aggression Detection (Sentiment score >0.8), Repetition Loop (цикличные неэффективные ответы).
3. Уровень Уверенности (Confidence-Based): NLU Confidence (< 0.7), Tool Failure (API error).

## 📦 Протокол передачи контекста (Anti-Dump Protocol)
Передача "Structured State" вместо лога чата (исследования XTrace):
1. Global Context (The "Why"): Долгосрочная цель.
2. Local Context (The "What"): Описание проблемы в последнем сообщении.
3. Persistence State (LangGraph Checkpointing): Точка в графе состояний (доступ к использованным инструментам).
4. Action Log: Список выполненных транзакций (API calls).

## ⏳ Архитектурные паттерны прерывания (Human-in-the-Loop)
- Interrupt-and-Verify: Приостановка действия до подтверждения человеком.
- Human-on-the-Side: ИИ готовит черновик, человек правит в CRM.
- Graceful Handover (Exotel Pattern): 30-секундный период параллельной активности сессии (Бот + Человек).

## 🛡️ Безопасность и Валидация
- Sensitive Key Masking: Маскировка PII (паспорта, номера карт) при передаче операторам в Slack/Telegram.

Источники: Fin AI, Exotel, XTrace, LangGraph (Persistence).
