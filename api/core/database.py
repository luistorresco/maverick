import mysql.connector
import os


def establish_database_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


def execute_query_with_retry(query, val=None, max_retries=3, retry_interval=1):
    retry_count = 0
    while True:
        try:
            mydb = establish_database_connection()
            mycursor = mydb.cursor()
            if val:
                mycursor.execute(query, val)
            else:
                mycursor.execute(query)
            if query.strip().lower().startswith("select"):
                result = mycursor.fetchall()
            else:
                mydb.commit()
                result = None
            mycursor.close()
            mydb.close()
            return result
        except mysql.connector.Error as e:
            if retry_count < max_retries:
                print(f"Error: {e}. Reintentando...")
                retry_count += 1
                time.sleep(retry_interval)
            else:
                raise HTTPException(
                    status_code=500, detail="Error en la base de datos"
                ) from e
