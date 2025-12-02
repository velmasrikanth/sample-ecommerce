Order Service (Go)

- Port: 5003 (default)
- Run:
  - `go build -o order-service .` in this folder
  - `./order-service` (on Windows `order-service.exe`)

Env vars (optional):
- `USER_SERVICE_URL` (default `http://localhost:5002`)
- `PRODUCT_SERVICE_URL` (default `http://localhost:5001`)

Endpoints:
- `GET /health` : health check
- `GET /orders` : list orders
- `POST /orders` : create order JSON `{ "user_id": 1, "product_id": 2, "quantity": 1 }` (validates user/product by calling their services)
