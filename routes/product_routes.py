from fastapi import APIRouter
from schemas.product import Product

router = APIRouter()


@router.get("/products")
def list_products():
    """
    List all available products.
    """
    # Logic to list all products here
    return {"products": []}


@router.get("/products/{product_id}")
def get_product_details(product_id: int):
    """
    Get details of a specific product.
    """
    # Logic to get product details here
    return {"product": "product details"}


@router.post("/products/add")
def add_product(product: Product):
    """
    Add a new product to the inventory.
    """
    # Logic to add a product here
    return {"message": "Product added successfully"}


@router.put("/products/update/{product_id}")
def update_product(product_id: int, product: Product):
    """
    Update the details of an existing product.
    """
    # Logic to update a product here
    return {"message": "Product updated successfully"}


@router.delete("/products/delete/{product_id}")
def delete_product(product_id: int):
    """
    Remove a product from the inventory.
    """
    # Logic to delete a product here
    return {"message": "Product deleted successfully"}
