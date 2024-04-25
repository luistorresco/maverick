from sqlalchemy import table, column, MetaData
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta

meta = MetaData()
products = table('products',  meta, column( 
                'id', Integer, primary_key=True), 
                column('name', String(255)),
                column('description', String(255)),
                column('price', Integer(255)))

meta.create_all(engine)
