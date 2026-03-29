from fastapi import FastAPI
from app.api.routes import search

app = FastAPI(title="Google Shopping SERP API")

app.include_router(search.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Google Shopping SERP API is running"}
