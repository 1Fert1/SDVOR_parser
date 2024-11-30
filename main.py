from fastapi import FastAPI, HTTPException
from database import SessionLocal, Product
import parser

app = FastAPI()

# Маршрут для запуска парсинга данных
@app.get("/parse")
def parse_data():
    parser.get_products()
    return {"message": "Парсинг завершён, данные сохранены в базе"}

# Получение всех товаров
@app.get("/products")
def get_products():
    db = SessionLocal()
    products = db.query(Product).all()
    db.close()
    return products

# Получение товара по ID
@app.get("/products/{product_id}")
def get_product(product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    db.close()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product

# Удаление товара по ID
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    db.delete(product)
    db.commit()
    db.close()
    return {"message": "Товар удален"}

# Обновление товара по ID
@app.put("/products/{product_id}")
def update_product(product_id: int, name: str, price: str):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    product.name = name
    product.price = price
    db.commit()
    db.close()
    return {"message": "Товар обновлён"}
