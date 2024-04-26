from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import mysql.connector
import time
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

# Configuración de la conexión a la base de datos MySQL
def establish_database_connection():
    return mysql.connector.connect(
        host="62.72.50.52",
        user="u317228138_store",
        password="1234567890qwertyuiop.M",
        database="u317228138_marketplace",
    )

# Función para ejecutar una consulta con reintento
def execute_query_with_retry(query, max_retries=3, retry_interval=1):
    retry_count = 0
    while True:
        try:
            # Establecer la conexión a la base de datos
            mydb = establish_database_connection()
            mycursor = mydb.cursor()

            # Ejecutar la consulta
            mycursor.execute(query)

            # Obtener los resultados y cerrar la conexión
            result = mycursor.fetchall()
            mycursor.close()
            mydb.close()

            # Devolver los resultados
            return result
        except mysql.connector.errors.OperationalError as e:
            if retry_count < max_retries:
                # Registrar el error
                print(f"Error: {e}. Reintentando...")
                # Incrementar el contador de reintento
                retry_count += 1
                # Esperar el intervalo de reintento
                time.sleep(retry_interval)
            else:
                # Si se excede el número máximo de reintentos, elevar el error
                raise e

# Definición del modelo de datos
class Shoe(BaseModel):
    """Represents a shoe item."""
    image: str
    size: float
    brand: str
    model: str
    offer: bool
    color: str

# Configuración de la aplicación FastAPI
app = FastAPI(
    title="storeShoes",
    version="2.3.1",
    description="This is an API for managing shoes in a store."
)

# Agregar etiquetas para agrupar las rutas
tags_metadata = [
    {"name": "Shoes", "description": "Operations related to shoes"},
    {"name": "Search", "description": "Operations for searching shoes"},
]

# Sobrescribir la función get_openapi para agregar las etiquetas
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="storeShoes",
        version="2.3.1",
        description="This is an API for managing shoes in a store.",
        routes=app.routes,
    )
    openapi_schema["tags"] = tags_metadata
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # Rutas CRUD para la entidad "zapatos"
@app.post("/shoes/", tags=["Shoes"], summary="Crear un nuevo zapato", description="Crear un nuevo elemento de zapato con los detalles proporcionados.")
async def create_shoe(shoe: dict):
    sql = "INSERT INTO shoes (brand, model, size, color) VALUES (%s, %s, %s, %s)"
    val = (shoe.get('brand'), shoe.get('model'), shoe.get('size'), shoe.get('color'))
    try:
        execute_query_with_retry(sql, val)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error al crear el zapato") from e
    return {"message": "Zapato creado exitosamente"}

@app.get("/shoes/", tags=["Shoes"], summary="Leer todos los zapatos", description="Recuperar todos los elementos de zapato.")
async def read_shoes():
    query = "SELECT * FROM shoes"
    try:
        shoes = execute_query_with_retry(query)
        if not shoes:
            raise HTTPException(status_code=404, detail="No se encontraron zapatos")
        formatted_shoes = []
        for shoe in shoes:
            formatted_shoe = {
                "id": shoe[0],
                "brand": shoe[1],
                "model": shoe[2],
                "size": shoe[3],
                "color": shoe[4],
                "image": shoe[5],
            }
            formatted_shoes.append(formatted_shoe)
        return formatted_shoes
    except:
        raise HTTPException(status_code=500, detail="Error al recuperar los zapatos")

@app.get("/shoes", tags=["Search"], summary="Buscar zapatos por color", description="Recuperar elementos de zapato filtrados por color.")
async def read_shoes_by_color(color: str = Query(None, description="Filtrar zapatos por color")):
    if color:
        query = "SELECT * FROM shoes WHERE color = %s"
        try:
            shoes = execute_query_with_retry(query, (color,))
        except:
            raise HTTPException(status_code=500, detail="Error al recuperar los zapatos")
    else:
        query = "SELECT * FROM shoes"
        try:
            shoes = execute_query_with_retry(query)
        except:
            raise HTTPException(status_code=500, detail="Error al recuperar los zapatos")
    if not shoes:
        raise HTTPException(status_code=404, detail="No se encontraron zapatos")
    return shoes

@app.put("/shoes/{shoe_id}", tags=["Shoes"], summary="Actualizar un zapato", description="Actualizar un elemento de zapato existente.")
async def update_shoe(shoe_id: int, shoe: dict):
    sql = "UPDATE shoes SET brand=%s, model=%s, size=%s, color=%s WHERE id=%s"
    val = (shoe.get("brand"), shoe.get("model"), shoe.get("size"), shoe.get("color"), shoe_id)
    try:
        execute_query_with_retry(sql, val)
    except:
        raise HTTPException(status_code=400, detail="Error al actualizar el zapato")
    return {"message": "Zapato actualizado exitosamente"}

@app.delete("/shoes/{shoe_id}", tags=["Shoes"], summary="Eliminar un zapato", description="Eliminar un elemento de zapato existente.")
async def delete_shoe(shoe_id: int):
    sql = "DELETE FROM shoes WHERE id = %s"
    val = (shoe_id,)
    try:
        execute_query_with_retry(sql, val)
    except:
        raise HTTPException(status_code=400, detail="Error al eliminar el zapato")
    return {"message": "Zapato eliminado exitosamente"}Rutas CRUD para la entidad "zapatos"
