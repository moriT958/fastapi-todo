from fastapi import FastAPI
from routers import auth


app = FastAPI()

@app.get('/')
async def route():
    return {"Hello,": "TodoApp!!!"}

app.include_router(auth.router)
# app.include_router()