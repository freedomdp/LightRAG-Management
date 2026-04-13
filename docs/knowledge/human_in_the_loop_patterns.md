# Human-in-the-Loop (HITL) и паттерны эскалации

Этот стандарт определяет, как ИИ-агент должен взаимодействовать с живым оператором (менеджером) и передавать ему управление диалогом.

## 🚨 Триггеры эскалации (Handoff Triggers)

Агент должен инициировать передачу человеку в следующих случаях:
1.  **Low Confidence Score**: ИИ не уверен в ответе (ниже 70-80%).
2.  **Out of Scope**: Клиент задает вопросы, не входящие в бизнес-роль агента.
3.  **Sentiment Alert**: Клиент проявляет гнев или явное недовольство.
4.  **Implicit Request**: Прямая просьба "Позови человека".
5.  **Critical Action**: Требуется аппрув финансовой операции.

## 📦 Payload: Правила передачи контекста

Главная ошибка проектирования — "Context Dump" (передача всей простыни чата). Оператор не должен читать 50 сообщений.
**HLV Standard Payload**:
- **Summary**: Краткая выжимка (что случилось, что уже решили).
- **Intent**: Текущая цель клиента.
- **Key Artifacts**: Собранные данные (Телефон, Адрес, Бюджет).
- **Timeline**: Краткая хронология событий.

## ⏳ HITL Архитектура: Interrupt & Wait

В n8n или LangGraph архитектуре используется паттерн **Wait**:
1.  ИИ готовит решение/ответ.
2.  Система ставится на "паузу" (Interrupt).
3.  Уведомление уходит менеджеру (Telegram/CRM).
4.  Менеджер жмет "Approve" или "Edit".
5.  ИИ возобновляет работу и отправляет результат клиенту.

> [!WARNING]
> Без структурированного Summary передача на человека превращается в хаос. Оператор тратит 2-3 минуты на чтение логов, что убивает ROI от внедрения ИИ.

---
**Источники**:
- [Fin AI: AI Agent Handoff Best Practices](https://fin.ai/glossary/ai-agent-handoff)
- [Exotel: Bot-to-Human Transfers Without Losing Context](https://exotel.com/blog/how-to-transfer-conversations-between-bots-and-humans/)
- [XTrace: Why Context Breaks & How to Fix It](https://xtrace.ai/blog/ai-agent-context-handoff)
