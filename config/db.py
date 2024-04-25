from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://u317228138_strores:Ukv52Knoy6U&@62.72.50.52/u317228138_strores")

meta = MetaData()
conn = engine.connect()
