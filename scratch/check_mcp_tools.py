import subprocess
import json

def main():
    try:
        proc = subprocess.Popen(
            ["/opt/homebrew/bin/notebooklm-mcp"], 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True,
            bufsize=1
        )
        
        def send(msg, id):
            msg["jsonrpc"] = "2.0"
            msg["id"] = id
            proc.stdin.write(json.dumps(msg) + "\n")
            proc.stdin.flush()
            return json.loads(proc.stdout.readline())

        send({"method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}}}, 1)
        proc.stdin.write('{"jsonrpc": "2.0", "method": "notifications/initialized"}\n')
        proc.stdin.flush()
        
        tools = send({"method": "tools/list", "params": {}}, 2)
        print(json.dumps(tools, indent=2))
        proc.terminate()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
