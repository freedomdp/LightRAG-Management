import urllib.request
import json
import os

def ingest_architecture():
    # Read the content of architecture.md
    with open('docs/architecture.md', 'r') as f:
        content = f.read()

    # Prepare the payload
    # Note: LightRAG POST /documents/text expects {"text": "...", "file_source": "..."}
    payload = {
        "text": content,
        "file_source": "docs/architecture.md"
    }
    
    data = json.dumps(payload).encode('utf-8')
    
    # Request setup
    req = urllib.request.Request(
        'http://localhost:9621/documents/text',
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            print(f"Success: {res_data}")
            return res_data
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    ingest_architecture()
