from fastapi import FastAPI


app = FastAPI()

@app.get('/')
async def route():
    return {"Hello,": "TodoApp!!!"}

# app.include_router()
# app.include_router()