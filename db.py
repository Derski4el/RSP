from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./products.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    price = Column(Integer, index=True)
    brand = Column(String, index=True)


def init_db():Base.metadata.create_all(bind=engine)


def seed_data():
    initial_products = [{"name": "Товар 1", "category": "Электроника", "price": 100, "brand": "Бренд A"},
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
        {"name": "Товар 16", "category": "Электроника", "price": 170, "brand": "Бренд C"}]

    db: Session = SessionLocal()
    if db.query(Product).first():
        db.close()
        return

    for item in initial_products:
        product = Product(**item)
        db.add(product)
    db.commit()
    db.close()
