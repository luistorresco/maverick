from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://u317228138_strores:~SpDKMl>P5@localhost:3306/u317228138_strores")

meta = MetaData()
conn = engine.connect()