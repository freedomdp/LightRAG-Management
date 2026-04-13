import requests
import json

questions = [
    "Каковы 3 главных технических риска миграции LightRAG на сервер Ryzen 9?",
    "Какие 5 скучных бизнесов помогут стать миллионером в 2026 году согласно базе?",
    "В чем основная проблема с файлом part1.md, которую мы решали вчера?",
    "Какую роль в проекте выполняет агент Antigravity согласно конституции?",
    "Какие инструменты MCP сейчас подключены к системе?",
    "Почему мы решили перейти с Qwen на Gemma 4?",
    "Какие преимущества дает использование Neo4j в связке с LightRAG?",
    "Что автор видео про Obsidian говорит о накоплении данных RAG?",
    "Какие настройки в .env критичны для работы Docker на Mac?",
    "Как LightRAG помогает преодолеть 'векторную слепоту' обычного поиска?"
]

for i, q in enumerate(questions):
    print(f"\n--- Вопрос {i+1}: {q} ---")
    response = requests.post("http://localhost:9621/query", 
                             json={"query": q, "mode": "hybrid"})
    if response.status_code == 200:
        print(response.json()["response"])
    else:
        print(f"Ошибка API: {response.status_code}")
