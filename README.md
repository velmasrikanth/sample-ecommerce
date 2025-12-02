Sample E-commerce Polyglot Microservices (Initial simple version)

Services:
- Gateway (FastAPI) - `services/gateway` - port 5000
- Product service (Python/Flask) - `services/product-service` - port 5001
- User service (Node/Express) - `services/user-service` - port 5002
- Order service (Go) - `services/order-service` - port 5003

Goal:
- Provide simple, independent services in different languages that can later be containerized and deployed to Docker Compose / Kubernetes.
- No Docker or Kubernetes files are included in this iteration — pure code only.

Quick start (running each service locally):

1) Product service (Python)

```powershell
cd services\product-service
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

2) User service (Node)

```powershell
cd services\user-service
npm install
npm start
```

3) Order service (Go)

```powershell
cd services\order-service
go build -o order-service .
./order-service
```
(Windows: `order-service.exe`)

4) Gateway (FastAPI)

```powershell
cd services\gateway
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Example flow (using gateway):

- Create a product:
  `curl -X POST http://localhost:5000/api/products -H "Content-Type: application/json" -d "{\"name\":\"Widget\",\"price\":9.99}"`

- Create a user:
  `curl -X POST http://localhost:5000/api/users -H "Content-Type: application/json" -d "{\"name\":\"Alice\",\"email\":\"a@b.com\"}"`

- Create an order:
  `curl -X POST http://localhost:5000/api/orders -H "Content-Type: application/json" -d "{\"user_id\":1,\"product_id\":1,\"quantity\":1}"`

Notes & next steps:
- Services use simple local storage (SQLite file for products, JSON file for users, in-memory store for orders).
- Env vars allow customizing service URLs for integration and containerization later.
 - Next iteration: add Dockerfiles, docker-compose, Kubernetes manifests, and persistent storage.

Docker Compose
----------------
You can build and run everything locally with Docker Compose (requires Docker):

```powershell
docker-compose up --build
```

Services will be accessible on the following ports:
 - Gateway: `http://localhost:5000`
 - Frontend: `http://localhost:8080`
 - Product: `http://localhost:5001`
 - User: `http://localhost:5002`
 - Order: `http://localhost:5003`

Notes:
 - Each service has a `Dockerfile` with per-line comments inside the `services/*` folders.
 - The `docker-compose.yml` sets container names and environment variables so services talk to each other by name.
