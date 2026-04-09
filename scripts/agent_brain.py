import requests
import json
import os

API_URL = "http://localhost:9621/query"

def query_brain(prompt, mode="hybrid"):
    """
    Отправляет запрос к LightRAG API.
    Режимы: 'hybrid' (рекомендуется), 'local', 'global', 'naive'.
    """
    payload = {
        "query": prompt,
        "mode": mode
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "Нет ответа от мозга.")
    except Exception as e:
        return f"Ошибка обращения к LightRAG: {str(e)}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"Запрос к мозгу: {query}\n")
        print("-" * 30)
        print(query_brain(query))
        print("-" * 30)
    else:
        print("Использование: python3 scripts/agent_brain.py 'Ваш вопрос'")
