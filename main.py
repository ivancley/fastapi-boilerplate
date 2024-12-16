from fastapi import FastAPI
from api.v1.context.controller import router as context_router  
from api.v1.user.controller import router as user_router

app = FastAPI()

app.include_router(context_router)
app.include_router(user_router)


@app.get("/status")
async def get_status():
    return {"message": "Api Funcionando"}