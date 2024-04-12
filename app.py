from fastapi import FastAPI
from routes.products import products

app = FastAPI()

app.include_router(products)