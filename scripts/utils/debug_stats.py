import json
import os

def debug():
    kv_path = "rag_storage/kv_store_doc_status.json"
    registry_path = "temp/ingest_registry.json"
    
    with open(kv_path, 'r') as f:
        kv_data = json.load(f)
        
    with open(registry_path, 'r') as f:
        registry = json.load(f)
        
    print(f"Registry size: {len(registry)}")
    print(f"KV store size: {len(kv_data)}")
    
    found = 0
    not_found = 0
    missing_ids = []
    
    for doc_id in registry:
        if doc_id in kv_data:
            status = kv_data[doc_id].get("status")
            if status == "processed":
                found += 1
            else:
                print(f"ID {doc_id} exists but status is: {status}")
        else:
            not_found += 1
            missing_ids.append(doc_id)
            
    print(f"--- MATCHING RESULTS ---")
    print(f"Found and Processed: {found}")
    print(f"Not found in KV: {not_found}")
    
    if missing_ids:
        print(f"First 5 missing IDs: {missing_ids[:5]}")
        # Let's see if these filenames exist in KV but with different IDs
        for mid in missing_ids[:3]:
            fname = registry[mid].get("filename")
            print(f"Searching for filename: {fname}")
            for k, v in kv_data.items():
                if v.get("file_path") and fname in v.get("file_path"):
                    print(f"  -> Found similar file in KV with ID: {k} (status: {v.get('status')}, path: {v.get('file_path')})")

if __name__ == "__main__":
    debug()
