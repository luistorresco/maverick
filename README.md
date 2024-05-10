# API de Gestión de Zapatos

Esta es una API para gestionar zapatos en una tienda. Permite realizar operaciones CRUD en elementos de zapatos.

## Instalación

Para ejecutar esta API localmente, sigue estos pasos:

1. Clona este repositorio: `git clone https://github.com/tu_usuario/tu_repositorio.git`
2. Instala las dependencias: `pip install -r requirements.txt`
3. Ejecuta la aplicación: `uvicorn main:app --reload`

## Uso

La API ofrece las siguientes rutas:

- `POST /shoes/`: Crea un nuevo zapato.
- `GET /shoes/`: Lee todos los zapatos.
- `GET /shoes?color={color}`: Busca zapatos por color.
- `PUT /shoes/{shoe_id}`: Actualiza un zapato existente.
- `DELETE /shoes/{shoe_id}`: Elimina un zapato existente.

Puedes encontrar más detalles sobre cómo usar cada ruta en la documentación de la API.

## Documentación de la API

La documentación de la API está disponible en `/docs` y `/redoc`. Puedes acceder a ella en tu navegador después de ejecutar la aplicación.

## Estructura de Carpetas

<div class="folder">app/
    <div class="sub-folder">├── api/
        <div class="file">│   ├── __init__.py</div>
        <div class="sub-folder">│   ├── endpoints/
            <div class="file">│   │   ├── __init__.py</div>
            <div class="file">│   │   └── shoes.py</div>
        </div>
    </div>
    <div class="sub-folder">├── core/
        <div class="file">│   ├── __init__.py</div>
        <div class="file">│   └── database.py</div>
    </div>
    <div class="sub-folder">├── models/
        <div class="file">│   ├── __init__.py</div>
        <div class="file">│   └── shoe.py</div>
    </div>
    <div class="file">└── main.py</div>
</div>






## Changelog
### [2.3.2] - 9 de mayo de 2024
#### Cambios
- Corregido un error en un endpoint específico.
- Mejoras en la consulta a la base de datos.
- Se agregó un nuevo endpoint para recuperar todos los elementos.
- Resolución de conflictos en el archivo requirements.txt

### [2.3.1] - 25 de abril de 2024
#### Cambios
- Corregido error en la serialización JSON en los endpoints.
- Mejoras en la consulta a la base de datos.
- Corregido un error en un endpoint específico.
- Se agregó un nuevo endpoint para recuperar todos los elementos.
- Se resolvieron conflictos en el archivo `requirements.txt`.

### [2.3.0] - 24 de abril de 2024
#### Cambios
- Actualización de dependencias.
- Mejoras en el archivo `products.py`.
- Correcciones en el archivo `db.py`.

### [1.0.0] - 11 de abril de 2024
#### Cambios
- ¡Primer lanzamiento de la API!
