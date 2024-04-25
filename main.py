from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import mysql.connector
import time

# Configuración de la conexión a la base de datos MySQL
def establish_database_connection():
    return mysql.connector.connect(
        host="62.72.50.52",
        user="u317228138_store",
        password="1234567890qwertyuiop.M",
        database="u317228138_marketplace"
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
    image: str
    size: float
    brand: str
    model: str
    offer: bool
    color: str

# Configuración de la aplicación FastAPI
app = FastAPI()

# Rutas CRUD para la entidad "zapatos"
@app.post("/shoes/")
async def create_shoe(shoe: Shoe):
    sql = "INSERT INTO shoes (brand, model, size, color) VALUES (%s, %s, %s, %s)"
    val = (shoe.brand, shoe.model, shoe.size, shoe.color)
    execute_query_with_retry(sql, val)
    return {"message": "Shoe created successfully"}

@app.get("/shoes/")
async def read_shoes():
    query = "SELECT * FROM shoes"
    shoes = execute_query_with_retry(query)
    formatted_shoes = []
    for shoe in shoes:
        formatted_shoe = {
            "albumId": 1,
            "id": shoe[0],
            "title": f"{shoe[1]} {shoe[2]}",
            "url": shoe[5],
            "thumbnailUrl": shoe[5]  # Usar la misma URL para la miniatura por ahora
        }
        formatted_shoes.append(formatted_shoe)
    return formatted_shoes

@app.get("/shoes", tags=["search"])
async def read_shoes_by_color(color: str = Query(None)):
    if color:
        query = "SELECT * FROM shoes WHERE color = %s"
        shoes = execute_query_with_retry(query, (color,))
    else:
        query = "SELECT * FROM shoes"
        shoes = execute_query_with_retry(query)
    if not shoes:
        raise HTTPException(status_code=404, detail="No shoes found")
    return shoes

@app.put("/shoes/{shoe_id}")
async def update_shoe(shoe_id: int, shoe: Shoe):
    sql = "UPDATE shoes SET brand=%s, model=%s, size=%s, color=%s WHERE id=%s"
    val = (shoe.brand, shoe.model, shoe.size, shoe.color, shoe_id)
    execute_query_with_retry(sql, val)
    return {"message": "Shoe updated successfully"}

@app.delete("/shoes/{shoe_id}")
async def delete_shoe(shoe_id: int):
    sql = "DELETE FROM shoes WHERE id = %s"
    val = (shoe_id,)
    execute_query_with_retry(sql, val)
    return {"message": "Shoe deleted successfully"}