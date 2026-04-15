import requests
import json

BASE_URL = "http://localhost:9621"

def check_health():
    try:
        res = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {res.json()}")
    except Exception as e:
        print(f"Error checking health: {e}")

def list_documents():
    # Попробуем получить список документов через гипотетический эндпоинт или логи
    # Если эндпоинта нет, мы просто сделаем тестовый запрос на сущности
    print("Checking for BrowserAct entities in the graph...")
    query_url = f"{BASE_URL}/query"
    payload = {
        "query": "BrowserAct",
        "mode": "hybrid",
        "only_need_context": True
    }
    try:
        res = requests.post(query_url, json=payload)
        data = res.json()
        print(f"Context found: {data.get('context')[:500] if data.get('context') else 'NO CONTEXT FOUND'}")
    except Exception as e:
        print(f"Error querying context: {e}")

if __name__ == "__main__":
    check_health()
    list_documents()
