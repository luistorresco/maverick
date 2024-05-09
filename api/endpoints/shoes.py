from fastapi import APIRouter, HTTPException
from core.database import execute_query_with_retry
from models.shoe import Shoe

router = APIRouter()


@router.post(
    "/shoes/",
    tags=["Shoes"],
    summary="Crear un nuevo zapato",
    description="Crear un nuevo elemento de zapato con los detalles proporcionados.",
)
async def create_shoe(shoe: Shoe):
    sql = "INSERT INTO shoes (brand, model, size, color, image) VALUES (%s, %s, %s, %s, %s)"
    val = (shoe.brand, shoe.model, shoe.size, shoe.color, shoe.image)
    try:
        execute_query_with_retry(sql, val)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error al crear el zapato") from e
    return {"message": "Zapato creado exitosamente"}


@app.get(
    "/shoes/",
    tags=["Shoes"],
    summary="Leer todos los zapatos",
    description="Recuperar todos los elementos de zapato.",
)
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error al recuperar los zapatos"
        ) from e


@app.get(
    "/shoes",
    tags=["Search"],
    summary="Buscar zapatos por color",
    description="Recuperar elementos de zapato filtrados por color.",
)
async def read_shoes_by_color(
    color: str = Query(None, description="Filtrar zapatos por color")
):
    if color:
        query = "SELECT * FROM shoes WHERE color = %s"
        try:
            shoes = execute_query_with_retry(query, (color,))
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
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="Error al recuperar los zapatos"
            ) from e
    else:
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
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="Error al recuperar los zapatos"
            ) from e


@app.put(
    "/shoes/{shoe_id}",
    tags=["Shoes"],
    summary="Actualizar un zapato",
    description="Actualizar un elemento de zapato existente.",
)
async def update_shoe(shoe_id: int, shoe: Shoe):
    sql = "UPDATE shoes SET brand=%s, model=%s, size=%s, color=%s, image=%s WHERE id=%s"
    val = (shoe.brand, shoe.model, shoe.size, shoe.color, shoe.image, shoe_id)
    try:
        execute_query_with_retry(sql, val)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400, detail="Error al actualizar el zapato"
        ) from e
    return {"message": "Zapato actualizado exitosamente"}


@app.delete(
    "/shoes/{shoe_id}",
    tags=["Shoes"],
    summary="Eliminar un zapato",
    description="Eliminar un elemento de zapato existente.",
)
async def delete_shoe(shoe_id: int):
    sql = "DELETE FROM shoes WHERE id = %s"
    val = (shoe_id,)
    try:
        execute_query_with_retry(sql, val)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400, detail="Error al eliminar el zapato"
        ) from e
    return {"message": "Zapato eliminado exitosamente"}
