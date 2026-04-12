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
EXPERIENCE_DIR = "/Users/sergej/StudioProjects/LightRAG/docs/experience"

def ingest_file(filepath):
    """Ingests a single file into LightRAG API."""
    logger.info(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        payload = {
            "text": content,
            "file_source": os.path.basename(filepath)
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            API_URL,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        # Increase timeout for large documents
        with urllib.request.urlopen(req, timeout=600) as response:
            res_data = json.loads(response.read().decode())
            logger.info(f"Successfully ingested {os.path.basename(filepath)}. API Response: {res_data}")
            return True
            
    except Exception as e:
        logger.error(f"Failed to ingest {filepath}: {str(e)}")
        return False

def main():
    if not os.path.exists(EXPERIENCE_DIR):
        logger.error(f"Directory {EXPERIENCE_DIR} not found.")
        return

    # List only our 10 skill files
    skill_files = [f for f in os.listdir(EXPERIENCE_DIR) if f.startswith('skill_') and f.endswith('.md')]
    skill_files.sort()
    
    if not skill_files:
        logger.warning(f"No skill files found in {EXPERIENCE_DIR}")
        return

    total = len(skill_files)
    logger.info(f"Found {total} skill documents for JIT ingestion.")
    
    for i, filename in enumerate(skill_files):
        current_idx = i + 1
        filepath = os.path.join(EXPERIENCE_DIR, filename)
        
        logger.info(f"[{current_idx}/{total}] Ingesting {filename}...")
        success = ingest_file(filepath)
        
        if success:
            time.sleep(2) # Safe delay for vector DB indexing
        else:
            logger.error(f"Failed to ingest {filename}, continuing with next...")

if __name__ == "__main__":
    main()
