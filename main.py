from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI(
    title="storeShoes",
    version="2.3.1",
    description="This is an API for managing shoes in a store."
)

# Configurar middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar y registrar los routers de los endpoints
from api.endpoints import shoes
app.include_router(shoes.router)

# Si necesitas más endpoints, importar y registrarlos aquí
# Ejemplo: app.include_router(otro_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
