import os
import json
import requests
from dotenv import load_dotenv

# Загрузка конфигурации
load_dotenv()

class PainAnalyser:
    def __init__(self):
        self.ollama_url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
        self.model = os.getenv("LLM_MODEL", "gemma4:e4b")

    def _ask_llm(self, prompt):
        """
        Запрос к локальной модели Ollama.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        try:
            response = requests.post(f"{self.ollama_url}/api/generate", json=payload)
            response.raise_for_status()
            return response.json().get("response")
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return None

    def analyse_lead(self, lead_data):
        """
        Анализ 100 отзывов и репутации компании.
        """
        biz_info = lead_data.get("business_info", {})
        reviews = lead_data.get("reputation_raw", [])
        
        # Формируем выборку отзывов для анализа (чтобы не перегрузить контекст)
        review_texts = []
        for r in reviews[:100]:
            r_text = f"Rating: {r.get('review_rating')} | Review: {r.get('review_text')} | Owner Reply: {r.get('owner_answer')}"
            review_texts.append(r_text)
            
        full_reviews_str = "\n".join(review_texts)

        prompt = f"""
        Analyze the following business reviews and owner responses. 
        Your goal is to extract "Business Pain Points" and "Reputation Gaps" for an AI Agency pitch.
        
        Business Name: {biz_info.get('name')}
        Niche: {biz_info.get('type')}
        
        Reviews (100 total):
        {full_reviews_str}
        
        Return a JSON object with:
        1. "top_3_pains": Key recurring complaints from customers.
        2. "reputation_audit": Analysis of owner replies (responsiveness, tone, handling of negative reviews).
        3. "ai_opportunity": Specific logic why this business needs AI automation (e.g., auto-responding to Google reviews, 24/7 lead capture).
        4. "landing_page_structure": 
           - "hero_headline_en": Catchy headline in English.
           - "hero_headline_es": Catchy headline in Spanish.
           - "value_points": 3 bullet points for the landing page.
        """

        analysis_json = self._ask_llm(prompt)
        return json.loads(analysis_json) if analysis_json else None

    def process_file(self, file_path):
        """
        Обработка всего JSON-файла с лидами из папки data/leads/.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            leads = json.load(f)
            
        results = []
        for lead in leads:
            biz_name = lead.get('business_info', {}).get('name')
            print(f"[*] Analyzing: {biz_name}...")
            
            analysis = self.analyse_lead(lead)
            if analysis:
                lead['analysis_dna'] = analysis
                results.append(lead)
                
        # Сохранение обогащенных данных
        output_path = file_path.replace(".json", "_ANALYZED.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
            
        print(f"[!] Analysis complete. Enriched Lead DNA saved to: {output_path}")
        return output_path

if __name__ == "__main__":
    analyser = PainAnalyser()
    # analyser.process_file("data/leads/example_leads.json")
