import json
import os

storage_path = "/Users/sergej/StudioProjects/LightRAG/rag_storage"

for filename in os.listdir(storage_path):
    if filename.endswith(".json"):
        file_path = os.path.join(storage_path, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                json.load(f)
            print(f"OK: {filename}")
        except json.JSONDecodeError as e:
            print(f"FAILED: {filename} - Error: {e}")
        except Exception as e:
            print(f"ERROR: {filename} - {str(e)}")
