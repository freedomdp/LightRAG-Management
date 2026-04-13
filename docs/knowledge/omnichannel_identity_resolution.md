# Архитектура Identity Resolution и Омниканальности (Expert-Level)

Этот документ определяет алгоритмы сквозной идентификации и логику управления графом идентичности в высоконагруженных омниканальных системах.

## 🔗 Логика склейки (Matching Logic)

Агент должен использовать два типа алгоритмов для связывания разрозненных данных в единый профиль (Golden Profile):

### 1. Детерминированное сопоставление (Deterministic Matching)
- **Принцип**: Использование проверенных уникальных идентификаторов.
- **Идентификаторы**: Email, User ID, Номер телефона, налоговые ID.
- **Точность**: 100%. Это фундамент, на котором строятся транзакционные системы.
- **Constraint**: Любое несовпадение детерминированных ID в рамках одной сессии должно приводить к разделению профиля или вызову гейта валидации.

### 2. Вероятностное сопоставление (Probabilistic Matching)
- **Принцип**: Статистическое моделирование вероятности того, что разные ID принадлежат одному человеку.
- **Параметры**: IP-адрес, тип устройства, версия браузера, геолокация.
- **Алгоритм**: Расчет "Similarity Score". Если score > пресетного порога (например, 0.95), профили объединяются временно до детерминированного подтверждения.

## 👤 Граф идентичности (Identity Graph)

Центральная база данных (Graph DB или профилировщик), связывающая все ID:
- **Profile IDs**: Мастер-ID пользователя.
- **Anonymous IDs**: Временные куки сесси на сайте.
- **External IDs**: ID из внешних систем (IDFA для iOS, Google Advertising ID, FB Scoped ID).

## ⚙️ Алгоритм разрешения (Real-time Resolution Flow)

1.  **COLLECT**: Сбор идентификаторов из всех источников (веб-события, логи бэкенда, CRM-данные).
2.  **MATCH**: Сравнение собранных ID с графом идентичности через детерминированные и вероятностные фильтры.
3.  **MERGE**: Объединение событий анонимного периода (Discovery Stage) с профилем авторизованного пользователя (Conversion Stage) в режиме реального времени.
4.  **ACTIVATE**: Немедленная передача обновленного профиля в маркетинговый стек и AI-агенту для персонализации.

## 🛡️ Ограничения и комплаенс (PII/GDPR)

- **Data Clean Rooms**: Работа с маркетинговыми данными без прямого доступа к PII (персонально идентифицируемой информации).
- **Consent Tracking**: Каждая идентификация должна быть связана с токеном согласия (Consent Token). Если клиент отозвал согласие на одном канале, граф идентичности должен заблокировать персонализацию во всех связанных каналах.

---
**Источники (Expert Reference)**:
- [Twilio Segment: Identity Resolution Fundamentals](https://segment.com/resources/fundamentals/identity-resolution/)
- [Twilio Segment: Identity Resolution Use-Cases](https://www.twilio.com/docs/segment/unify/identity-resolution/use-cases)
- [Twilio Blog: Identity Resolution Insights](https://www.twilio.com/en-us/blog/insights/identity-resolution)
- [Twilio Resource Center: Customer Identity (Cookieless)](https://www.twilio.com/en-us/resource-center/customer-identity-in-a-cookieless-world)
