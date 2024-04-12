from fastapi import APIRouter
from config.db import conn
from models.products import products


products = APIRouter()

@products.get("/products")
def read_products():
    return {"products": "all products"}

@products.get("/products")
def read_products():
    return {"products": "all products"}

@products.get("/products")
def read_products():
    return {"products": "all products"}

@products.get("/products")
def read_products():
    return {"products": "all products"}

@products.get("/products")
def read_products():
    return {"products": "all products"}
