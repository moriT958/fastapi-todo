from fastapi import FastAPI
from routers import todo, auth
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.get("/")
async def route():
    return {"Hello": "World!!!"}


app.include_router(todo.router)
app.include_router(auth.router)
