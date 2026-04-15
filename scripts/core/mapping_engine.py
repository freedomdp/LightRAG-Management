import os
import json
from datetime import datetime
from dotenv import load_dotenv
from outscraper import OutscraperClient

# Загрузка конфигурации
load_dotenv()

class MappingEngine:
    def __init__(self):
        self.api_key = os.getenv("OUTSCRAPER_API_KEY")
        if not self.api_key:
            print("WARNING: OUTSCRAPER_API_KEY not found in .env")
        self.client = OutscraperClient(api_key=self.api_key) if self.api_key else None

    def search_businesses(self, query, limit=10):
        """
        Поиск компаний по запросу (например, 'Roofing San Diego').
        """
        if not self.client:
            return {"error": "API Key missing"}

        print(f"[*] Searching for: {query} (Limit: {limit})...")
        results = self.client.google_maps_search(
            [query],
            limit=limit,
            language='en'
        )
        return results[0] if results else []

    def get_deep_reviews(self, place_id, limit=100):
        """
        Извлечение 100 отзывов и ответов владельца.
        """
        if not self.client:
            return []

        print(f"[*] Fetching {limit} reviews for {place_id}...")
        results = self.client.google_maps_reviews(
            [place_id],
            reviews_limit=limit,
            language='en'
        )
        return results[0].get('reviews_data', []) if results else []

    def execute_mapping(self, niche, city, limit_businesses=5):
        """
        Полный этап M: Поиск + Глубокий сбор отзывов.
        """
        query = f"{niche} in {city}"
        businesses = self.search_businesses(query, limit=limit_businesses)
        
        leads = []
        for biz in businesses:
            name = biz.get('name')
            place_id = biz.get('place_id')
            print(f"[+] Processing: {name}")
            
            # Собираем отзывы и ответы
            reviews = self.get_deep_reviews(place_id, limit=100)
            
            lead_data = {
                "business_info": biz,
                "reputation_raw": reviews,
                "scraped_at": datetime.now().isoformat()
            }
            leads.append(lead_data)
        
        # Сохранение результата
        output_dir = "data/leads"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{niche.replace(' ', '_')}_{city.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        
        path = os.path.join(output_dir, filename)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(leads, f, indent=4, ensure_ascii=False)
            
        print(f"[!] Success. Data saved to: {path}")
        return path

if __name__ == "__main__":
    # Пример вызова для теста (нужен ключ в .env)
    engine = MappingEngine()
    # engine.execute_mapping("AC Repair", "San Diego", limit_businesses=3)
