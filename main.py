from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from typing import List, Dict, Optional
import uvicorn

app = FastAPI()

products: List[Dict[str, str]] = [
    {"name": "Товар 1", "category": "Электроника", "price": 100, "brand": "Бренд A"},
    {"name": "Товар 2", "category": "Косметика", "price": 150, "brand": "Бренд B"},
    {"name": "Товар 3", "category": "Косметика", "price": 50, "brand": "Бренд A"},
    {"name": "Товар 4", "category": "Одежда", "price": 70, "brand": "Бренд C"},
    {"name": "Товар 5", "category": "Электроника", "price": 120, "brand": "Бренд A"},
    {"name": "Товар 6", "category": "Одежда", "price": 80, "brand": "Бренд B"},
    {"name": "Товар 7", "category": "Косметика", "price": 90, "brand": "Бренд C"},
    {"name": "Товар 8", "category": "Электроника", "price": 130, "brand": "Бренд A"},
    {"name": "Товар 9", "category": "Одежда", "price": 100, "brand": "Бренд B"},
    {"name": "Товар 10", "category": "Косметика", "price": 110, "brand": "Бренд C"},
    {"name": "Товар 11", "category": "Электроника", "price": 120, "brand": "Бренд A"},
    {"name": "Товар 12", "category": "Одежда", "price": 130, "brand": "Бренд B"},
    {"name": "Товар 13", "category": "Одежда", "price": 140, "brand": "Бренд C"},
    {"name": "Товар 14", "category": "Косметика", "price": 150, "brand": "Бренд A"},
    {"name": "Товар 15", "category": "Одежда", "price": 160, "brand": "Бренд B"},
    {"name": "Товар 16", "category": "Электроника", "price": 170, "brand": "Бренд C"},
]

templates = Jinja2Templates(directory="templates")

def filter_products(products: List[Dict[str, str]],
    name: Optional[str],
    category: Optional[str],
    price_min: Optional[str],
    price_max: Optional[str],
    brand: Optional[str]) -> List[Dict[str, str]]:

    filtered_products = []

    for product in products:
        match_found = True

        if name and name.lower() not in product['name'].lower(): match_found = False
        if category and category.lower() not in product['category'].lower(): match_found = False
        if price_min:
            try:
                price_min_value = int(price_min)
                if product['price'] < price_min_value: match_found = False
            except ValueError: match_found = False

        if price_max:
            try:
                price_max_value = int(price_max)
                if product['price'] > price_max_value:
                    match_found = False
            except ValueError: match_found = False
        if brand and brand.lower() not in product['brand'].lower(): match_found = False
        if match_found: filtered_products.append(product)
    return filtered_products

def paginate_products(products: List[Dict[str, str]], page: int, size: int) -> List[Dict[str, str]]:
    start = (page - 1) * size
    end = start + size
    return products[start:end]

@app.get("/", response_class=HTMLResponse)
async def read_products(request: Request, page: int = 1, size: int = 5):

    paginated_products = paginate_products(products, page, size)

    return templates.TemplateResponse("list.html", {"request": request, "products": paginated_products, "page": page, "size": size})

@app.get("/search", response_class=HTMLResponse)
async def search_products(request: Request,
    name: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    price_min: Optional[str] = Query(None),
    price_max: Optional[str] = Query(None),
    brand: Optional[str] = Query(None),
    page: int = 1,
    size: int = 5):

    filtered_products = filter_products(products, name, category, price_min, price_max, brand)

    paginated_products = paginate_products(filtered_products, page, size)

    return templates.TemplateResponse("list.html", {"request": request, "products": paginated_products, "page": page, "size": size})

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)





