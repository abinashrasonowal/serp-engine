from fastapi import FastAPI
from app.api.routes import search
from app.core.logging_config import setup_logging

# Initialize logging
setup_logging()

app = FastAPI(title="Google Shopping SERP API")

app.include_router(search.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Google Shopping SERP API is running"}
