# Омниканальность и Identity Resolution (Склейка профилей)

Этот документ описывает архитектуру сквозной идентификации клиента при разработке ИИ-агентов для бизнеса.

## 🔗 Identity Resolution: От Анонима к Клиенту

Агент не должен относиться к одному иону, написавшему в разные каналы, как к разным людям. 
- **Anonymous ID**: ID сессии на сайте (Cookies).
- **User ID**: Авторизованный профиль (Email, Телефон).
- **Merge Logic**: Процесс связывания действий анонима с конкретным клиентом в CRM после того, как он оставил контактные данные.

## 👤 Unified Customer Profile (UCP)

Централизованное хранилище данных, которое содержит:
1.  **Identity Graph**: Список всех ID связанных с человеком (Devices, Social IDs).
2.  **Event Stream**: История всех касаний во всех каналах.
3.  **State Logic**: Текущий статус клиента в воронке.

## 🧠 State & Memory Management

В омниканальной среде критически важно управление **Thread ID**:
- При переходе из WhatsApp в Telegram, система должна опознать клиента и передать новому коннектору тот же `Thread ID`.
- Это позволяет ИИ "поднять" контекст предыдущих 50 сообщений и не переспрашивать то, что уже было сказано.

> [!TIP]
> ИИ-архитектор должен проектировать систему так, чтобы NLP-ядро было "канало-независимым". Входными данными должен быть нормализованный JSON, содержащий `Message`, `User_Context` и `Identity_Token`.

---
**Источники**:
- [Twilio Segment: Identity Resolution Use-Cases](https://www.twilio.com/docs/segment/unify/identity-resolution/use-cases)
- [LangGraph: Conceptual Guide to Memory and State](https://langchain-ai.github.io/langgraph/concepts/memory/)
