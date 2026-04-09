import urllib.request
import json

def verify_knowledge():
    query = "Какова роль Neo4j в этом проекте?"
    payload = {
        "query": query,
        "mode": "hybrid",
        "stream": False
    }
    
    data = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request(
        'http://localhost:9621/query',
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    print(f"Querying: {query}")
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            print(f"Response: {res_data['response']}")
            return res_data
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    verify_knowledge()
