import json
import os
import time

def heal():
    kv_path = "rag_storage/kv_store_doc_status.json"
    registry_path = "temp/ingest_registry.json"
    knowledge_dir = "docs/knowledge"
    
    if not os.path.exists(kv_path):
        print(f"Error: {kv_path} not found")
        return
        
    with open(kv_path, 'r') as f:
        kv_data = json.load(f)
        
    # Start with a clean registry (v2.0 - Strict matching)
    registry = {}
            
    # Step 1: Scan current physical files
    knowledge_files = []
    for root, _, files in os.walk(knowledge_dir):
        for file in files:
            if file.endswith(".md"):
                rel_path = os.path.relpath(os.path.join(root, file), os.getcwd())
                knowledge_files.append(rel_path)

    print(f"Found {len(knowledge_files)} physical files in {knowledge_dir}")

    # Step 2: Match each file to the BEST doc_id in KV store
    added = 0
    file_to_best_match = {}

    # Pre-calculate filename lookup for fallback
    filename_to_doc = {}
    for doc_id, info in kv_data.items():
        fp = info.get("file_path")
        if fp:
            fname = os.path.basename(fp)
            if fname not in filename_to_doc or doc_id > filename_to_doc[fname]["doc_id"]:
                filename_to_doc[fname] = {"doc_id": doc_id, "info": info}

    for kf in knowledge_files:
        kf_basename = os.path.basename(kf)
        best_match = None
        
        # Priority 1: Exact Path Match
        for doc_id, info in kv_data.items():
            if info.get("file_path") == kf:
                best_match = {"doc_id": doc_id, "info": info}
                break # Exact match is best
        
        # Priority 2: Filename Match (Handle Move)
        if not best_match and kf_basename in filename_to_doc:
            best_match = filename_to_doc[kf_basename]
            
        if best_match:
            doc_id = best_match["doc_id"]
            info = best_match["info"]
            registry[doc_id] = {
                "filename": os.path.basename(kf),
                "registered_at": info.get("created_at_ts", 0) or 1776119400.0
            }
            added += 1
                
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=2)
        
    print(f"Registry rebuild complete! Mapped {added} files. Total in registry: {len(registry)}")

if __name__ == "__main__":
    heal()
