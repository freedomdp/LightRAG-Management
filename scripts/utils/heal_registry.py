import json
import os
import time
from datetime import datetime

def heal():
    kv_path = "rag_storage/kv_store_doc_status.json"
    registry_path = "temp/ingest_registry.json"
    log_path = "temp/heal_log.txt"
    knowledge_dir = "docs/knowledge"
    
    if not os.path.exists(kv_path):
        print(f"Error: {kv_path} not found")
        return
        
    with open(kv_path, 'r') as f:
        kv_data = json.load(f)
        
    # Step 0: Reset stuck 'processing' status
    resets = 0
    now_ts = time.time()
    for doc_id, info in kv_data.items():
        if info.get("status") == "processing":
            # If it has been in processing too long (or we just want to force reset)
            # In surgical mode, we reset all 'processing' to 'pending' to allow retry
            info["status"] = "pending"
            resets += 1
    
    if resets > 0:
        with open(kv_path, 'w') as f:
            json.dump(kv_data, f, indent=2)
        print(f"Surgical Reset: {resets} documents moved from 'processing' to 'pending'")

    # Start with a clean registry (v2.0 - Strict matching)
    registry = {}
            
    # Step 1: Scan current physical files
    knowledge_files = []
    for root, _, files in os.walk(knowledge_dir):
        for file in files:
            if file.endswith(".md"):
                rel_path = os.path.relpath(os.path.join(root, file), os.getcwd())
                knowledge_files.append(rel_path)

    log_entries = [f"Heal Session: {datetime.now().isoformat()}", f"Found {len(knowledge_files)} physical files"]

    # Step 2: Match each file to the BEST doc_id in KV store
    added = 0
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
                break 
        
        # Priority 2: Filename Match (Handle Move)
        if not best_match and kf_basename in filename_to_doc:
            best_match = filename_to_doc[kf_basename]
            log_entries.append(f"REMAP: {kf_basename} matched via filename to ID {best_match['doc_id']}")
            
        if best_match:
            doc_id = best_match["doc_id"]
            info = best_match["info"]
            registry[doc_id] = {
                "filename": os.path.basename(kf),
                "registered_at": info.get("created_at_ts", 0) or 1776119400.0,
                "status": info.get("status")
            }
            added += 1
        else:
            log_entries.append(f"MISSING: {kf} has no entry in KV store")
                
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=2)
    
    with open(log_path, 'w') as f:
        f.write("\n".join(log_entries))
        
    print(f"Registry rebuild complete! Mapped {added} files. Log written to {log_path}")

if __name__ == "__main__":
    heal()
