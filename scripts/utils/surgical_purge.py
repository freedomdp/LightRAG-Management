import json
import urllib.request
import os
import sys

def surgical_purge(target_statuses=["failed", "pending"], target_ids=None):
    status_path = "/Users/sergej/StudioProjects/LightRAG/rag_storage/kv_store_doc_status.json"
    api_url = "http://localhost:9621/documents/delete_document"
    
    if not os.path.exists(status_path):
        print(f"Error: status file not found at {status_path}")
        return

    with open(status_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return

    # Find IDs to delete
    ids_to_purge = []
    if target_ids:
        ids_to_purge = [tid for tid in target_ids if tid in data]
    else:
        for doc_id, doc_info in data.items():
            if doc_info.get("status") in target_statuses:
                ids_to_purge.append(doc_id)

    if not ids_to_purge:
        print(f"No documents found with statuses {target_statuses} to delete.")
        return

    print(f"Found {len(ids_to_purge)} documents to purge. Sending delete requests...")

    # Batch into chunks of 50
    chunk_size = 50
    success_count = 0
    
    for i in range(0, len(ids_to_purge), chunk_size):
        chunk = ids_to_purge[i:i + chunk_size]
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
    # If run directly as script, purge failed and pending
    surgical_purge()
