from fastapi import FastAPI
from backend.routes.ai_routes import router as ai_router

app = FastAPI(
    title="MedAI Backend",
    version="1.0"
)

app.include_router(ai_router)

@app.get("/")
def root():
    return {"message": "MedAI API running"}