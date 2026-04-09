import json
import os

# Пути
OUTPUT_FILE = "/Users/sergej/.gemini/antigravity/brain/44a4f92b-b8ee-46de-bdab-7f2f1cf4b5f7/.system_generated/steps/1952/output.txt"
STATUS_FILE = "/Users/sergej/StudioProjects/LightRAG/scripts/ingest_status.json"

def generate_status():
    if not os.path.exists(OUTPUT_FILE):
        print(f"Error: {OUTPUT_FILE} not found")
        return

    with open(OUTPUT_FILE, 'r') as f:
        data = json.load(f)

    # Путь к списку источников в структуре NotebookLM
    sources = data.get("notebook", [])[0][1]
    
    status_data = []
    for src in sources:
        source_id = src[0][0]
        name = src[1]
        status_data.append({
            "id": source_id,
            "name": name,
            "status": "pending",  # pending, downloaded, indexed
            "local_path": f"docs/notebook_content/{name.replace('/', '_')}.md"
        })

    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(status_data, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated status for {len(status_data)} sources.")

if __name__ == "__main__":
    generate_status()
