from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import mysql.connector

# Conexión a la base de datos MySQL
mydb = mysql.connector.connect(
    host="62.72.50.52",
    user="u317228138_store",
    password="1234567890qwertyuiop.M",
    database="u317228138_marketplace"
)
mycursor = mydb.cursor()

# Creación de la tabla "shoes" si no existe
# mycursor.execute("CREATE TABLE IF NOT EXISTS shoes (id INT AUTO_INCREMENT PRIMARY KEY, brand VARCHAR(255), model VARCHAR(255), size FLOAT, color VARCHAR(255))")
# Este código supone que tienes una conexión de base de datos activa y un cursor llamado `mycursor`.
# Lista de columnas requeridas con su tipo de dato correspondiente.
required_columns = {
    'id': 'INT AUTO_INCREMENT PRIMARY KEY',
    'brand': 'VARCHAR(255)',
    'model': 'VARCHAR(255)',
    'size': 'FLOAT',
    'color': 'VARCHAR(255)',
    'image': 'VARCHAR(255)',
    'offer': 'BOOLEAN'
}

# Verifica si la tabla existe.
mycursor.execute("SHOW TABLES LIKE 'shoes'")
table_exists = mycursor.fetchone()

if not table_exists:
    # Si la tabla no existe, crea la tabla con todas las columnas.
    create_table_statement = "CREATE TABLE shoes ("
    create_table_statement += ", ".join(["{} {}".format(column, datatype) for column, datatype in required_columns.items()])
    create_table_statement += ")"
    mycursor.execute(create_table_statement)
else:
    # Si la tabla existe, verifica si cada columna requerida también existe.
    for column_name, column_type in required_columns.items():
        mycursor.execute("SHOW COLUMNS FROM shoes LIKE %s", (column_name,))
        column_exists = mycursor.fetchone()
        
        if not column_exists:
            # Si la columna no existe, añádela a la tabla.
            alter_table_statement = "ALTER TABLE shoes ADD {} {}".format(column_name, column_type)
            mycursor.execute(alter_table_statement)

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
    mycursor.execute(sql, val)
    mydb.commit()
    return {"message": "Shoe created successfully"}

@app.get("/shoes/")
async def read_shoes():
    mycursor.execute("SELECT * FROM shoes")
    shoes = mycursor.fetchall()
    return shoes

@app.get("/shoes", tags=["search"])
async def read_shoes_by_color(color: str = Query(None)):
    if color:
        mycursor.execute("SELECT * FROM shoes WHERE color = %s", (color,))
    else:
        mycursor.execute("SELECT * FROM shoes")
    shoes = mycursor.fetchall()
    if not shoes:
        raise HTTPException(status_code=404, detail="No shoes found")
    return shoes

@app.put("/shoes/{shoe_id}")
async def update_shoe(shoe_id: int, shoe: Shoe):
    sql = "UPDATE shoes SET brand=%s, model=%s, size=%s, color=%s WHERE id=%s"
    val = (shoe.brand, shoe.model, shoe.size, shoe.color, shoe_id)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"message": "Shoe updated successfully"}

@app.delete("/shoes/{shoe_id}")
async def delete_shoe(shoe_id: int):
    mycursor.execute("DELETE FROM shoes WHERE id = %s", (shoe_id,))
    mydb.commit()
    return {"message": "Shoe deleted successfully"}
