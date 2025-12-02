from fastapi import FastAPI, Request, HTTPException
import httpx
import os

app = FastAPI()

USER_SVC = os.getenv('USER_SERVICE_URL', 'http://localhost:5002')
PRODUCT_SVC = os.getenv('PRODUCT_SERVICE_URL', 'http://localhost:5001')
ORDER_SVC = os.getenv('ORDER_SERVICE_URL', 'http://localhost:5003')

@app.get('/health')
async def health():
    return {"status": "ok"}

@app.get('/api/products')
async def proxy_products():
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{PRODUCT_SVC}/products")
        return r.json()

@app.post('/api/products')
async def proxy_create_product(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as c:
        r = await c.post(f"{PRODUCT_SVC}/products", json=body)
        if r.status_code >= 400:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        return r.json()

@app.get('/api/users')
async def proxy_users():
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{USER_SVC}/users")
        return r.json()

@app.post('/api/users')
async def proxy_create_user(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as c:
        r = await c.post(f"{USER_SVC}/users", json=body)
        if r.status_code >= 400:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        return r.json()

@app.get('/api/orders')
async def proxy_orders():
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{ORDER_SVC}/orders")
        return r.json()

@app.post('/api/orders')
async def proxy_create_order(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as c:
        r = await c.post(f"{ORDER_SVC}/orders", json=body)
        if r.status_code >= 400:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        return r.json()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
