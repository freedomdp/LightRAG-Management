# Проектирование Handoff и Human-in-the-Loop (Expert-Level)

Этот стандарт определяет технические алгоритмы эскалации и передачи контекста между ИИ-агентами и человеком, минимизируя "Context Breakdown".

## 🚨 Многоуровневые триггеры эскалации

Эскалация (Handoff) срабатывает на трех уровнях анализа:

### 1. Уровень Намерений (Intent-Based)
- **Direct Request**: Ключевые фразы "говорить с человеком", "оператор", "менеджер".
- **Scope Violation**: Определение через Zero-shot классификацию, что запрос не относится к разрешенному набору инструментов агента.

### 2. Уровень Эмоций (Sentiment-Based)
- **Aggression Detection**: Рост негативного sentiment score (>0.8 по шкале агрессии).
- **Repetition Loop**: Детекция цикличных запросов, на которые агент дает идентичные или неэффективные ответы.

### 3. Уровень Уверенности (Confidence-Based)
- **NLU Confidence**: Если вероятность распознавания интента < Threshold (обычно 0.7).
- **Tool Failure**: Если внешний API вернул ошибку, которую агент не может обработать самостоятельно.

## 📦 Протокол передачи контекста (Anti-Dump Protocol)

Согласно исследованиям XTrace, "Context Dump" (передача лога чата) — это антипаттерн. Оператор должен получать "Structured State":

1.  **Global Context (The "Why")**: Долгосрочная цель клиента, выявленная в начале беседы.
2.  **Local Context (The "What")**: Краткое описание проблемы в последнем сообщении.
3.  **Persistence State (LangGraph Checkpointing)**: Ссылка на сохраненную точку в графе состояний, позволяющую менеджеру увидеть не только текст, но и какие инструменты (API-вызовы) агент уже пытался использовать.
4.  **Action Log**: Список выполненных транзакций (например, "Бюджет подтвержден: 50к", "Email проверен").

## ⏳ Архитектурные паттерны прерывания (Human-in-the-Loop)

Для обеспечения надежности (Reliability) внедряются следующие режимы:

- **Interrupt-and-Verify**: Выполнение действия (например, удаление данных) приостанавливается до подтверждения человеком.
- **Human-on-the-Side**: ИИ готовит черновик ответа, человек правит его в CRM перед отправкой.
- **Graceful Handover (Exotel Pattern)**: Состояние сессии "активно" в обоих мирах (Бот и Человек) в течение 30 секунд после передачи, чтобы избежать обрыва связи до момента первого ответа оператора.

## 🛡️ Безопасность и Валидация
- **Sensitive Key Masking**: Все PII данные (паспорта, полные номера карт) должны маскироваться при передаче во внутренние каналы (Slack/Telegram) операторам.

---
**Источники (Expert Reference)**:
- [Fin AI: AI Agent Handoff Best Practices](https://fin.ai/glossary/ai-agent-handoff)
- [Exotel: Bot-to-Human Transfers Without Losing Context](https://exotel.com/blog/how-to-transfer-conversations-between-bots-and-humans/)
- [XTrace: Why Context Breaks & How to Fix It](https://xtrace.ai/blog/ai-agent-context-handoff)
- [LangChain Graph: Persistence & State Management](https://langchain-ai.github.io/langgraph/how-tos/persistence/)
