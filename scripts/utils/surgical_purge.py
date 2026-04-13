import json
import urllib.request
import os

def surgical_purge_failed():
    status_path = "/Users/sergej/StudioProjects/LightRAG/rag_storage/kv_store_doc_status.json"
    api_url = "http://localhost:9621/documents/delete_document"
    
    if not os.path.exists(status_path):
        print(f"Error: status file not found at {status_path}")
        return

    print(f"Reading status: {status_path}")
    with open(status_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return

    # Находим все ID со статусом failed
    failed_ids = []
    for doc_id, doc_info in data.items():
        if doc_info.get("status") == "failed":
            failed_ids.append(doc_id)

    if not failed_ids:
        print("No 'failed' documents found to delete.")
        return

    print(f"Found {len(failed_ids)} 'failed' documents. Sending delete requests...")

    # Разбиваем на чанки по 50
    chunk_size = 50
    success_count = 0
    
    for i in range(0, len(failed_ids), chunk_size):
        chunk = failed_ids[i:i + chunk_size]
        payload = {
            "doc_ids": chunk,
            "delete_file": False,
            "delete_llm_cache": True
        }
        
        encoded_data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            api_url,
            data=encoded_data,
            headers={'Content-Type': 'application/json'},
            method='DELETE'
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode())
                print(f"Chunk {i//chunk_size + 1} Success: {res_data}")
                success_count += len(chunk)
        except Exception as e:
            print(f"Chunk {i//chunk_size + 1} Error: {e}")

    print(f"Purge complete. Successfully sent deletion requests for {success_count} documents.")
    return success_count > 0

if __name__ == "__main__":
    surgical_purge_failed()
