# n8n v2.14.2: Docker Sidecar Infrastructure

## 1. Architecture: n8n + Browserless
For this project, n8n is not a standalone app but part of a Docker stack. 
- **Sidecar Concept**: Browserless is a "sidecar" service. It runs in its own container but is accessible locally at `http://browserless:3000`.

## 2. Connectivity Experience
- **DNS Resolution**: Inside the Docker network, use the service name `browserless` instead of `localhost` or `127.0.0.1`.
- **Port Mapping**: The service listens on `3000`. The host (user) can see it at `127.0.0.1:3000`, but n8n (another container) MUST use `browserless:3000`.

## 3. Persistence
- **Volumes**: n8n configuration, sessions, and credentials are stored in the `/home/node/.n8n` directory inside the container, mapped to a local volume.
- **Critical Lesson**: Never delete docker volumes without a backup of `database.sqlite` (if using SQLite), as it contains all workflow encryption keys and credentials.

## 4. Resource Management
Browserless Chrome is resource-heavy. 
- **Experience**: Running more than 5 concurrent browser tabs in small VPS instances can crash the stack. 
- **Solution**: Always use the **Loop (Split in Batches)** pattern in n8n (covered in Doc 12) with a batch size of `1-3` to keep memory usage low.

## 5. LightRAG Rule
When modifying `docker-compose.yml`, always check if the `networks` are correctly linked between n8n and browserless. If connectivity fails, suggest checking the service names in the Docker network.
