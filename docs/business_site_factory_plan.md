# 🚀 План "Бизнес-Автоматизация 3.0": Universal Niche Dominator

## 1. Концепция: "Система М.О.Н.Е.Й." (Modular Orchestration & Niche Expansion Yield)
Мы строим универсальную машину, которая может за 24 часа запустить экспансию в любую новую нишу. Основа — фреймворк Джека Робертса, усиленный агентской памятью LightRAG.

---

## 2. Архитектура "Универсального Конвейера"

### Stage 1: Mapping & Intelligence (M)
- **Universal Niche Engine**: Переключаемые пресеты для скрейпинга (например: "Plumbing", "Roofing", "HVAC").
- **Competitor Tech-Spy**: Автоматическое определение CRM и виджетов на сайтах конкурентов.
- **Sentiment Mirroring**: Выделение болей клиентов именно в выбранном городе/нише для формирования текстов.

### Stage 2: Lead Acquisition & Enrichment (O)
- **Extraction**: Скрейпинг Google Maps (Outscraper API).
- **Enrichment (The Paid Stack)**: 
    - **Anymail Finder API**: Поиск личных email владельцев (B2B почта).
    - **Lusha/Hunter (Optional)**: Дополнительная верификация контактов.
- **Lead Scoring**: Авто-фильтрация компаний с низким рейтингом или устаревшим дизайном сайта.

### Stage 3: Automated Nailing (N) - "Free Value First"
- **Clone & Customize Workflow**:
    1.  Берется "Золотой шаблон" ниши.
    2.  n8n через **WordPress REST API** или **Elementor JSON** меняет: 
        - Логотип клиента (генерация через SVG-skill или поиск).
        - Имя компании и контакты.
        - Отзывы (3-4 топовых отзыва с Google Maps).
    3.  Генерация уникального URL-превью (например: `business.freedomdp.pro/preview/[client-name]`).

### Stage 4: Execution & Outreach (E)
- **Instantly.ai Integration**:
    - Загрузка лидов в кампанию через API.
    - Использование динамических переменных: `{{preview_url}}`, `{{top_pain_point}}`.
    - **Strategy**: Email с текстом: *"Я уже подготовил новую версию вашего сайта на базе отзывов ваших клиентов. Посмотреть можно здесь: {{preview_url}}. Если интересно обсудить — ответьте на это письмо"*.

### Stage 5: Yield & Scale (Y)
- **Subscription Model**: $150–$300/мес за хостинг и поддержку.
- **Upsell Path**: 
    1. Интеграция ИИ-агента для записи клиентов.
    2. SMS-напоминания (Twilio).
    3. CRM-автоматизация (HubSpot/GoHighLevel).

---

## 🛠️ Технический Стэк и Затраты (Approved)
- **Sourcing**: Outscraper (~$25/10k leads).
- **Enrichment**: Anymail Finder (~$50/mo).
- **Outreach**: Instantly (~$37/mo + domain setup).
- **Orchestration**: n8n (Self-hosted).
- **CMS**: WordPress Multisite / Wildcard domains для быстрой генерации превью.

---

## 🛡️ Validation Gates
1.  **Email Deliverability**: Проверка доменов (SPF/DKIM/DMARC) перед началом рассылки.
2.  **Preview Integrity**: Роботизированная проверка битых ссылок на созданных превью-лендингах.
3.  **Client Privacy**: Соответствие GDPR/CCPA при обработке B2B данных.

---
*Документ утвержден как финальная спецификация для реализации промышленного конвейера. (V3.0)*
