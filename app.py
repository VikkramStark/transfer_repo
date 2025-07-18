from fastapi import FastAPI, Depends, APIRouter 
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse
import uvicorn 

from mysql.connector import pooling, MySQLConnection  
app = FastAPI()  

from dotenv import load_dotenv
import os 

load_dotenv() 

HOST = os.getenv('DB_HOST') 
USERNAME = os.getenv('DB_USER')
PASSWORD = os.getenv("DB_PASSWORD") 
PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")

print("Configs: ") 
print(HOST, USERNAME, PASSWORD, PORT, DB_NAME) 

connection_pool = pooling.MySQLConnectionPool(
    pool_name = "DB_Pool", 
    pool_size = 20, 
    pool_reset_session=True, 
    host = HOST, 
    user = USERNAME, 
    password = PASSWORD,
    port = PORT, 
    database = DB_NAME
)

def get_db():        
    conn = connection_pool.get_connection()  
    try:
        yield conn 
    finally:
        conn.close()  


@app.get("/") 
def home():
    return JSONResponse({'message':"Server Started Successfully"})

@app.get("/latest_data")
def latest_data(conn: MySQLConnection = Depends(get_db)):
    cursor = conn.cursor(dictionary=True) 
    sql = "select * from ioc_attributes;" 
    cursor.execute(sql) 
    result = cursor.fetchall()
    cursor.close()
    return result
    # return JSONResponse(content = result if result else {"message":"No Data"}) 

@app.get("/ioc_values")
def ioc_values(ioc_type:str,conn: MySQLConnection = Depends(get_db)):
    cursor = conn.cursor(dictionary=False) 
    sql = f'select ioc_value from ioc_attributes where ioc_type = "{ioc_type}";' 
    cursor.execute(sql) 
    res = cursor.fetchall()  
    cursor.close()

    result = [] 
    for i in res:
        result.append(i[0]) 
    result = "\n".join(i for i in result)
    return PlainTextResponse(result) 
    

    


# @app.get("/db_data") 
# def database_data():
#     sql = "select * from ioc_attributes;" 
#     cursor.execute(sql) 
#     data = cursor.fetchall() 
#     return data


PORT = 5000
if __name__ == "__main__":
    uvicorn.run("app:app", port = PORT, host = '0.0.0.0', reload = True)    