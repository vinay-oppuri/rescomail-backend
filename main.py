from fastapi import FastAPI
from api import upload

app = FastAPI()

app.include_router(upload.router)

@app.get("/")
def home():
    return {"message": "Server is running"}