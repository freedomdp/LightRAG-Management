import urllib.request
import json
import os
import time
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

API_URL = "http://localhost:9621/documents/text"
CONTENT_DIR = "docs/notebook_content"
STATUS_FILE = "temp/ingest_status.json"

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

def ingest_file(filepath):
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
            logger.info(f"Successfully ingested {filepath}. API Response: {res_data}")
            return True
            
    except urllib.error.URLError as e:
        logger.error(f"Network error processing {filepath}: {e}")
        return False
    except Exception as e:
        logger.error(f"Error successfully requesting {filepath}: {e}, skipping to next...")
        return False
        logger.error(f"Failed to ingest {filepath}: {str(e)}")
        return False

def main():
    if not os.path.exists(CONTENT_DIR):
        logger.error(f"Directory {CONTENT_DIR} not found.")
        return

    files = sorted([f for f in os.listdir(CONTENT_DIR) if f.endswith('.md')])
    if not files:
        logger.warning(f"No .md files found in {CONTENT_DIR}")
        return

    total = len(files)
    logger.info(f"Found {total} files for ingestion.")
    
    for i, filename in enumerate(files):
        current_idx = i + 1
        filepath = os.path.join(CONTENT_DIR, filename)
        
        logger.info(f"[{current_idx}/{total}] Ingesting {filename}...")
        update_status(current_idx, total, filename)
        
        success = ingest_file(filepath)
        
        if success:
            time.sleep(1) # Delay between documents
        else:
            logger.error(f"Failed to ingest {filename}, continuing with next...")

if __name__ == "__main__":
    main()

