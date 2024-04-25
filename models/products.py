from sqlalchemy import Table, Column, MetaData, Integer, String
from config.db import engine

meta = MetaData()

products = Table('products', meta,
                 Column('id', Integer, primary_key=True),
                 Column('name', String(255)),
                 Column('description', String(255)),
                 Column('price', Integer))

meta.create_all(engine)
