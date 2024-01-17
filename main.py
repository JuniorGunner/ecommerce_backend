from fastapi import FastAPI
from routes import (
    user_routes,
    product_routes,
    order_routes,
    cart_routes,
    analytics_routes
)

app = FastAPI()

# Including different route modules
app.include_router(user_routes.router)
app.include_router(product_routes.router)
app.include_router(order_routes.router)
app.include_router(cart_routes.router)
app.include_router(analytics_routes.router)
