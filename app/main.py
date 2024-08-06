from fastapi import FastAPI
from routers import todo, auth

app = FastAPI()

@app.get('/')
async def route():
    return {"Hello,": "TodoApp!!!"}

app.include_router(todo.router)
app.include_router(auth.router)