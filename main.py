from fastapi import FastAPI, Query, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from typing import Optional, List
from contextlib import asynccontextmanager
import uvicorn

from db import Product, SessionLocal, init_db, seed_data

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_data()
    yield


app = FastAPI(lifespan=lifespan)


def filter_products_query(
    db: Session,
    name: Optional[str],
    category: Optional[str],
    price_min: Optional[str],
    price_max: Optional[str],
    brand: Optional[str]) -> List[Product]:

    query = db.query(Product)

    if name: query = query.filter(Product.name.ilike(f"%{name}%"))
    if category: query = query.filter(Product.category.ilike(f"%{category}%"))
    if brand: query = query.filter(Product.brand.ilike(f"%{brand}%"))

    if price_min:
        try:
            price_min_value = int(price_min)
            query = query.filter(Product.price >= price_min_value)
        except ValueError: pass

    if price_max:
        try:
            price_max_value = int(price_max)
            query = query.filter(Product.price <= price_max_value)
        except ValueError: pass

    return query


def paginate_query(query, page: int, size: int): return query.offset((page - 1) * size).limit(size).all()


@app.get("/", response_class=HTMLResponse)
async def read_products(request: Request, page: int = 1, size: int = 5, db: Session = Depends(get_db)):
    query = db.query(Product)
    paginated = paginate_query(query, page, size)
    return templates.TemplateResponse("list.html",
        {"request": request,
        "products": paginated,
        "page": page,
        "size": size})


@app.get("/search", response_class=HTMLResponse)
async def search_products(request: Request,
    name: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    price_min: Optional[str] = Query(None),
    price_max: Optional[str] = Query(None),
    brand: Optional[str] = Query(None),
    page: int = 1, size: int = 5,
    db: Session = Depends(get_db)):
    query = filter_products_query(db, name, category, price_min, price_max, brand)
    paginated = paginate_query(query, page, size)
    return templates.TemplateResponse("list.html", 
        {"request": request,
        "products": paginated,
        "page": page,
        "size": size})


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
