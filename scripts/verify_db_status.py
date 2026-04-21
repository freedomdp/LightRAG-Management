import requests
import os
import json
import time
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

NEO4J_URI = "http://localhost:7474/db/neo4j/tx/commit"
NEO4J_USER = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

def verify_node_count():
    print("🔍 Проверка состояния базы данных Neo4j...")
    
    query = {"statements": [{"statement": "MATCH (n) RETURN count(n) as count"}]}
    
    try:
        response = requests.post(
            NEO4J_URI,
            auth=(NEO4J_USER, NEO4J_PASSWORD),
            json=query,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            count = data['results'][0]['data'][0]['row'][0]
            print(f"✅ Успешно! Обнаружено узлов в графе: {count}")
            if count >= 21000:
                print("💎 База данных в полной сохранности (21k+ узлов подтверждено).")
            else:
                print(f"⚠️ Внимание: Обнаружено только {count} узлов. Ожидалось 21,000+.")
            return count
        else:
            print(f"❌ Ошибка подключения к Neo4j: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Критическая ошибка при проверке: {str(e)}")
        return None

if __name__ == "__main__":
    # Даем базе немного времени на прогрев, если скрипт запущен сразу после старта
    verify_node_count()
