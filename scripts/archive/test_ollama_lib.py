import ollama
import asyncio
import os

async def test():
    host = os.environ.get('OLLAMA_BASE_URL', 'http://host.docker.internal:11434')
    print(f"Testing connectivity to: {host}")
    client = ollama.AsyncClient(host=host)
    try:
        models = await client.list()
        print(f"Successfully connected! Models: {models}")
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    asyncio.run(test())
