import requests
import json
import argparse

API_URL = "http://localhost:9621/query"

def ask_lightrag(query_text, mode="hybrid", style="encyclopedia"):
    # Промпты для разных стилей
    style_prompts = {
        "friendly": "Отвечай как живой, дружелюбный и современный консультант. Используй легкий, но профессиональный стиль. Избегай сухого академического тона. Если чего-то не знаешь, вежливо извинись. Вопрос пользователя: ",
        "pro": "Отвечай как технический эксперт, глубоко знающий систему. Будь точен в деталях, но пиши доступным языком. Вопрос пользователя: ",
        "encyclopedia": "" # Стандартный стиль
    }
    
    final_query = style_prompts.get(style, "") + query_text
    
    payload = {
        "query": final_query,
        "mode": mode,
        "only_need_context": False
    }
    
    print(f"\n🧠 Думаю в стиле '{style}' (режим: {mode})...\n")
    try:
        response = requests.post(API_URL, json=payload, timeout=600)
        if response.status_code == 200:
            result = response.json()
            answer = result.get("response") or result.get("data") or result
            
            print(f"--- [ ИСТОЧНИК: ЛОКАЛЬНАЯ БАЗА | СТИЛЬ: {style.upper()} ] ---")
            print(f"📊 Статус: Ответ сформирован на основе вашего графа Neo4j")
            print("=========================================")
            print(answer)
            print("=========================================")
        else:
            print(f"❌ Ошибка API: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Ошибка соединения: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Запрос к базе знаний LightRAG")
    parser.add_argument("query", type=str, help="Ваш вопрос в кавычках")
    parser.add_argument("--mode", type=str, default="hybrid", choices=["local", "global", "hybrid", "naive"], help="Режим поиска (по умолчанию hybrid)")
    parser.add_argument("--style", type=str, default="encyclopedia", choices=["friendly", "pro", "encyclopedia"], help="Стиль ответа (по умолчанию encyclopedia)")
    
    args = parser.parse_args()
    ask_lightrag(args.query, args.mode, args.style)
