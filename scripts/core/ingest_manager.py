import urllib.request
import json
import os
import time
import logging
import hashlib
import re
import subprocess

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

API_URL = "http://localhost:9621/documents/text"
# Directories containing documents for RAG
DOCUMENT_DIRS = [
    "docs/knowledge",
    "docs/experience"
]
STATUS_FILE = "temp/ingest_status.json"
REGISTRY_FILE = "temp/ingest_registry.json"

def run_backup():
    """Triggers automated safety backup before ingestion."""
    try:
        script_path = os.path.join(os.path.dirname(__file__), "backup_manager.py")
        logger.info("📦 [Integrity Guard] Triggering pre-ingest safety backup...")
        subprocess.run(["python3", script_path, "--backup", "--label", "pre_ingest", "--cleanup"], check=True)
    except Exception as e:
        logger.error(f"❌ Automatic backup failed: {e}")

def update_status(current, total, filename):
    try:
        os.makedirs("temp", exist_ok=True)
        with open(STATUS_FILE, "w") as f:
            json.dump({
                "current": current,
                "total": total,
                "last_file": filename,
                "timestamp": time.time()
            }, f)
    except Exception as e:
        logger.error(f"Failed to update status file: {e}")

def register_mapping(doc_id, filename):
    try:
        os.makedirs("temp", exist_ok=True)
        registry = {}
        if os.path.exists(REGISTRY_FILE):
            with open(REGISTRY_FILE, "r") as f:
                registry = json.load(f)
        
        registry[doc_id] = {
            "filename": filename,
            "registered_at": time.time(),
            "status": "processed"
        }
        
        with open(REGISTRY_FILE, "w") as f:
            json.dump(registry, f, indent=2)
        logger.info(f"Registered mapping: {doc_id} -> {filename}")
    except Exception as e:
        logger.error(f"Failed to update registry: {e}")

def ingest_file(filepath, rel_filename):
    """Ingests a single file into LightRAG API."""
    logger.info(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        payload = {
            "text": content,
            "file_source": filepath
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            API_URL,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=3600) as response:
            res_data = json.loads(response.read().decode())
            
            # Try to extract doc_id from response
            doc_id = res_data.get("doc_id")
            
            # If duplicated, doc_id is in the message string
            if not doc_id and res_data.get("status") == "duplicated":
                message = res_data.get("message", "")
                match = re.search(r"doc_id: (doc-[a-f0-9]+)", message)
                if match:
                    doc_id = match.group(1)
            
            if doc_id:
                register_mapping(doc_id, rel_filename)
                logger.info(f"Successfully processed {filepath}. DocID: {doc_id}")
            elif res_data.get("status") == "duplicated" and "processed" in res_data.get("message", "").lower():
                # Use a unique key for the registry to avoid overwriting duplicates
                file_hash = hashlib.md5(rel_filename.encode()).hexdigest()
                register_mapping(f"doc-hash-{file_hash}", rel_filename)
                logger.info(f"File {rel_filename} already exists in DB. Registered with hash key.")

            else:
                logger.warning(f"Could not resolve DocID for {filepath}. API Response: {res_data}")

            
            return True
            
    except urllib.error.URLError as e:
        logger.error(f"Network error processing {filepath}: {e}")
        return False
    except Exception as e:
        logger.error(f"Error successfully requesting {filepath}: {e}")
        return False

def main():
    # Recursive search for .md files across all configured directories
    all_files_info = []
    for directory in DOCUMENT_DIRS:
        if not os.path.exists(directory):
            logger.warning(f"Directory {directory} not found, skipping...")
            continue
            
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.md'):
                    abs_path = os.path.join(root, file)
                    # We use relative path from the current working directory as the unique key
                    rel_path = os.path.relpath(abs_path, os.getcwd())
                    all_files_info.append({"abs": abs_path, "rel": rel_path})
    
    all_files_info.sort(key=lambda x: x["rel"])
    
    if not all_files_info:
        logger.warning(f"No .md files found in {DOCUMENT_DIRS}")
        return

    total = len(all_files_info)
    logger.info(f"Found {total} files for ingestion across {len(DOCUMENT_DIRS)} directories.")
    
    # Trigger safety backup before ingestion starts
    run_backup()
    
    for i, file_info in enumerate(all_files_info):
        current_idx = i + 1
        filepath = file_info["abs"]
        rel_filename = file_info["rel"]
        
        # Check if file is already in registry to skip processing
        registry = {}
        if os.path.exists(REGISTRY_FILE):
            try:
                with open(REGISTRY_FILE, "r") as f:
                    registry = json.load(f)
            except:
                pass
        
        # Check if file is already processed in registry to skip
        processed_entry = next((v for v in registry.values() if v.get("filename") == rel_filename), None)
        if processed_entry and processed_entry.get("status") == "processed":
            logger.info(f"[{current_idx}/{total}] Skipping {rel_filename} (Already processed)")
            continue

        logger.info(f"[{current_idx}/{total}] Ingesting {rel_filename}...")
        update_status(current_idx, total, rel_filename)
        
        success = ingest_file(filepath, rel_filename)
        
        if success:
            # Short delay for system stability
            time.sleep(12) 
        else:
            logger.error(f"Failed to ingest {rel_filename}, continuing with next...")

if __name__ == "__main__":
    main()

