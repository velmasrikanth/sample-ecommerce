Gateway (FastAPI)

- Port: 5000
- Run:
  - Create and activate virtualenv
  - `pip install -r requirements.txt`
  - `python app.py` or `uvicorn app:app --host 0.0.0.0 --port 5000`

Routes:
- `GET /health`
- `GET /api/products`, `POST /api/products`
- `GET /api/users`, `POST /api/users`
- `GET /api/orders`, `POST /api/orders`

This gateway proxies requests to the underlying services running on their default ports.
