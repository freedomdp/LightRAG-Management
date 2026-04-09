import subprocess
import json
import time
import os

def run_command(cmd, timeout=10):
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Error: Command timed out"
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

def get_neo4j_stats():
    # Запрос к cypher-shell внутри контейнера
    cmd = 'docker exec lightrag_neo4j cypher-shell -u neo4j -p lightrag_pass_123 "MATCH (n) RETURN count(n) as nodes; MATCH ()-[r]->() RETURN count(r) as relationships;"'
    output = run_command(cmd)
    
    if "Error" in output:
        return {"nodes": 0, "rels": 0, "error": output}
    
    # Парсинг вывода cypher-shell
    try:
        lines = output.split('\n')
        nodes = int(lines[1]) if len(lines) > 1 else 0
        rels = int(lines[len(lines)-1]) if len(lines) > 3 else 0
        return {"nodes": nodes, "rels": rels}
    except:
        return {"nodes": "N/A", "rels": "N/A", "error": f"Parse error: {output}"}

def get_qdrant_stats():
    # Запрос к API Qdrant через curl
    cmd = 'curl -s --max-time 5 http://localhost:6333/collections'
    collections_data = run_command(cmd)
    if "Error" in collections_data:
        return {"error": collections_data}
    
    try:
        result = json.loads(collections_data).get("result", {})
        if not result:
            return {"error": "No result from Qdrant"}
            
        collections = result.get("collections", [])
        stats = {}
        for col in collections:
            name = col["name"]
            count_cmd = f'curl -s --max-time 5 http://localhost:6333/collections/{name}'
            col_info = json.loads(run_command(count_cmd))
            points = col_info.get("result", {}).get("points_count", 0)
            stats[name] = points
        return stats
    except Exception as e:
        return {"error": f"Parse error: {str(e)}"}

def main():
    print("="*40)
    print("LIGHTRAG DATABASE MONITOR")
    print("="*40)
    
    while True:
        stats_neo = get_neo4j_stats()
        stats_qdrant = get_qdrant_stats()
        
        print(f"\n[{time.strftime('%H:%M:%S')}] --- Status ---")
        print(f"Neo4j: {stats_neo.get('nodes')} nodes, {stats_neo.get('rels')} relationships")
        print(f"Qdrant: {stats_qdrant}")
        
        time.sleep(10)

if __name__ == "__main__":
    main()

