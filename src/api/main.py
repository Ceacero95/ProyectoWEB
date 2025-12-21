from fastapi import FastAPI
from src.db.connector import execute_query

app = FastAPI()

@app.get("/data")
def read_data():
    res = execute_query("SELECT * FROM project_data LIMIT 10", fetch_results=True)
    return {"data": res}
