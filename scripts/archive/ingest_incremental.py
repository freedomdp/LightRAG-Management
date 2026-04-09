import urllib.request
import json
import os
import time
import sys

# Configuration
API_URL = 'http://localhost:9621/documents/text'
TIMEOUT = 600  # 10 minutes timeout for heavy graph extraction
RETRY_DELAY = 10

def ingest_text(text, source_name):
    print(f"[*] Ingesting: {source_name} ({len(text)} chars)...")
    payload = {
        "text": text,
        "file_source": source_name
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    start_time = time.time()
    try:
        # Using context manager for urllib request
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            res_data = json.loads(response.read().decode())
            duration = time.time() - start_time
            print(f"[+] Success: {source_name} processed in {duration:.2f}s")
            return res_data
    except Exception as e:
        duration = time.time() - start_time
        print(f"[!] Error processing {source_name} after {duration:.2f}s: {e}")
        return None

def main():
    content_dir = 'docs/notebook_content'
    if not os.path.exists(content_dir):
        print(f"[!] Directory {content_dir} not found. Use extraction script first.")
        return

    # Get all .txt files
    files = [f for f in os.listdir(content_dir) if f.endswith('.txt')]
    files.sort()
    
    print(f"[*] Found {len(files)} documents to ingest.")
    
    for i, filename in enumerate(files):
        print(f"\n--- Document {i+1}/{len(files)} ---")
        file_path = os.path.join(content_dir, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        result = ingest_text(content, f"notebook_content/{filename}")
        
        if result:
            # Just to give Ollama a tiny breather between heavy tasks
            time.sleep(2)
        else:
            print("[!] Skipping to next file after failure.")

if __name__ == "__main__":
    main()
