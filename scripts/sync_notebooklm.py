import subprocess
import json
import os
import sys

# IDs of documents to fetch (read from temp/source_ids.txt)
SOURCE_IDS_FILE = "temp/source_ids.txt"
OUTPUT_DIR = "docs/notebook_content"

def send_request(proc, req, req_id):
    req["jsonrpc"] = "2.0"
    req["id"] = req_id
    proc.stdin.write(json.dumps(req) + "\n")
    proc.stdin.flush()
    line = proc.stdout.readline()
    if not line:
        return None
    try:
        return json.loads(line)
    except Exception as e:
        print(f"Error parsing JSON: {line}")
        return None

def main():
    if not os.path.exists(SOURCE_IDS_FILE):
        print(f"File {SOURCE_IDS_FILE} not found!")
        return
        
    with open(SOURCE_IDS_FILE, 'r') as f:
        source_ids = [line.strip() for line in f if line.strip()]
        
    print(f"Found {len(source_ids)} sources to sync.")

    try:
        proc = subprocess.Popen(
            ["/opt/homebrew/bin/notebooklm-mcp"], 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True,
            bufsize=1
        )
    except Exception as e:
        print(f"Error starting mcp: {e}")
        return

    # Init
    init_msg = {
        "method": "initialize", 
        "params": {
            "protocolVersion": "2024-11-05", 
            "capabilities": {}, 
            "clientInfo": {"name": "sync", "version": "1"}
        }
    }
    send_request(proc, init_msg, 1)
    
    proc.stdin.write('{"jsonrpc": "2.0", "method": "notifications/initialized"}\n')
    proc.stdin.flush()
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Process all sources
    for idx, source_id in enumerate(source_ids):
        print(f"[{idx+1}/{len(source_ids)}] Fetching source {source_id}...")
        
        # Get source info first to get the title
        info_msg = {
            "method": "tools/call",
            "params": {
                "name": "source_describe",
                "arguments": {"source_id": source_id}
            }
        }
        res_info = send_request(proc, info_msg, 2 + idx*2)
        
        title = source_id
        if res_info and "result" in res_info and "content" in res_info["result"]:
            try:
                # The content usually contains JSON string with `title`
                text_content = res_info["result"]["content"][0]["text"]
                source_meta = json.loads(text_content)
                title = source_meta.get("title", source_id)
            except:
                pass
                
        # Sanitize title
        clean_title = "".join([c if c.isalnum() else "_" for c in title])
        file_path = os.path.join(OUTPUT_DIR, f"{clean_title}.md")
        
        # Skip if file already exists
        if os.path.exists(file_path):
            print(f" -> Cached: {clean_title}")
            continue

        # Get content
        call_msg = {
            "method": "tools/call",
            "params": {
                "name": "source_get_content",
                "arguments": {"source_id": source_id}
            }
        }
        
        res_content = send_request(proc, call_msg, 3 + idx*2)
        if res_content and "result" in res_content and "content" in res_content["result"]:
            text = res_content["result"]["content"][0]["text"]
            
            with open(file_path, 'w') as f:
                f.write(text)
            print(f" -> Saved: {clean_title}.md")
        else:
            print(f" -> Error fetching content")

    proc.terminate()
    print("Done downloading sources!")

if __name__ == "__main__":
    main()
