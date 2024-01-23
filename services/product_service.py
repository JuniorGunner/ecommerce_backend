from sqlalchemy.orm import Session
from models.product import ProductModel
from schemas.product import ProductSchema


def get_products(db: Session):
    return db.query(ProductModel).all()


def get_product(db: Session, product_id: int):
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()


def create_product(db: Session, product: ProductSchema):
    db_product = ProductModel(name=product.name, description=product.description, price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product: ProductSchema):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db.commit()
        db.refresh(db_product)
        return db_product
    return None


def delete_product(db: Session, product_id: int):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False
