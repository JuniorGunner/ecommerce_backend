from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.product import ProductSchema
from services import product_service
from services.user_service import oauth2_scheme, get_current_user

router = APIRouter()


@router.get("/products")
def list_products(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    List all available products.
    """
    products = product_service.get_products(db)
    return {"products": products}


@router.get("/products/{product_id}")
def get_product_details(
    product_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    """
    Get details of a specific product.
    """
    product = product_service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product": product}


@router.post("/products/add", response_model=ProductSchema)
def add_product(
    product: ProductSchema,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """
    Add a new product to the inventory.
    """
    return product_service.create_product(db, product)


@router.put("/products/update/{product_id}", response_model=ProductSchema)
def update_product(
    product_id: int,
    product: ProductSchema,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """
    Update the details of an existing product.
    """
    updated_product = product_service.update_product(db, product_id, product)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@router.delete("/products/delete/{product_id}")
def delete_product(
    product_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    """
    Remove a product from the inventory.
    """
    success = product_service.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
