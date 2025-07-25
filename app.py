from fastapi import FastAPI
from src.api_v1.main_router import router


app = FastAPI()

app.include_router(router)
