Product Service (Python/Flask)

- Port: 5001
- Run:
  - Create a virtualenv: `python -m venv .venv`
  - Activate it on PowerShell: `.\.venv\Scripts\Activate.ps1`
  - Install: `pip install -r requirements.txt`
  - Run: `python app.py`

Endpoints:
- `GET /health` : health check
- `GET /products` : list products
- `GET /products/<id>` : get a product
- `POST /products` : create product JSON `{ "name": "Name", "price": 9.99 }`
