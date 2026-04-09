import urllib.request
import json

def delete_doc(doc_id):
    payload = {
        "document_ids": [doc_id],
        "delete_file": True,
        "delete_llm_cache": True
    }
    
    data = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request(
        'http://localhost:9621/documents/delete_document',
        data=data,
        headers={'Content-Type': 'application/json'},
        method='DELETE'
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
    delete_doc("doc-57c54f8e192e625d24cc539fde434a5f")
