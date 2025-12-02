from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
import logging

app = FastAPI()

# allow the frontend dev server(s) to access the gateway
app.add_middleware(
    CORSMiddleware,
    # Development-friendly: allow all origins so the frontend served from
    # the VM IP or any dev server can call the gateway. Replace with a
    # specific origin list for production.
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("uvicorn.error")

USER_SVC = os.getenv('USER_SERVICE_URL', 'http://localhost:5002')
PRODUCT_SVC = os.getenv('PRODUCT_SERVICE_URL', 'http://localhost:5001')
ORDER_SVC = os.getenv('ORDER_SERVICE_URL', 'http://localhost:5003')

@app.get('/health')
async def health():
    return {"status": "ok"}

@app.get('/api/products')
async def proxy_products():
    try:
        async with httpx.AsyncClient(timeout=5.0) as c:
            r = await c.get(f"{PRODUCT_SVC}/products")
    except httpx.RequestError as e:
        logger.exception("Error contacting product service")
        raise HTTPException(status_code=502, detail=str(e))

    try:
        content = r.json()
    except Exception:
        content = r.text
    return JSONResponse(content=content, status_code=r.status_code)

@app.post('/api/products')
async def proxy_create_product(request: Request):
    body = await request.json()
    try:
        async with httpx.AsyncClient(timeout=5.0) as c:
            r = await c.post(f"{PRODUCT_SVC}/products", json=body)
    except httpx.RequestError as e:
        logger.exception("Error contacting product service")
        raise HTTPException(status_code=502, detail=str(e))

    try:
        content = r.json()
    except Exception:
        content = r.text

    if r.status_code >= 400:
        raise HTTPException(status_code=r.status_code, detail=content)
    return JSONResponse(content=content, status_code=r.status_code)

@app.get('/api/users')
async def proxy_users():
    try:
        async with httpx.AsyncClient(timeout=5.0) as c:
            r = await c.get(f"{USER_SVC}/users")
    except httpx.RequestError as e:
        logger.exception("Error contacting user service")
        raise HTTPException(status_code=502, detail=str(e))

    try:
        content = r.json()
    except Exception:
        content = r.text
    return JSONResponse(content=content, status_code=r.status_code)

@app.post('/api/users')
async def proxy_create_user(request: Request):
    body = await request.json()
    try:
        async with httpx.AsyncClient(timeout=5.0) as c:
            r = await c.post(f"{USER_SVC}/users", json=body)
    except httpx.RequestError as e:
        logger.exception("Error contacting user service")
        raise HTTPException(status_code=502, detail=str(e))

    try:
        content = r.json()
    except Exception:
        content = r.text

    if r.status_code >= 400:
        raise HTTPException(status_code=r.status_code, detail=content)
    return JSONResponse(content=content, status_code=r.status_code)

@app.get('/api/orders')
async def proxy_orders():
    try:
        async with httpx.AsyncClient(timeout=5.0) as c:
            r = await c.get(f"{ORDER_SVC}/orders")
    except httpx.RequestError as e:
        logger.exception("Error contacting order service")
        raise HTTPException(status_code=502, detail=str(e))

    try:
        content = r.json()
    except Exception:
        content = r.text
    return JSONResponse(content=content, status_code=r.status_code)

@app.post('/api/orders')
async def proxy_create_order(request: Request):
    body = await request.json()
    try:
        async with httpx.AsyncClient(timeout=5.0) as c:
            r = await c.post(f"{ORDER_SVC}/orders", json=body)
    except httpx.RequestError as e:
        logger.exception("Error contacting order service")
        raise HTTPException(status_code=502, detail=str(e))

    try:
        content = r.json()
    except Exception:
        content = r.text

    if r.status_code >= 400:
        raise HTTPException(status_code=r.status_code, detail=content)
    return JSONResponse(content=content, status_code=r.status_code)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
