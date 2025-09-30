from fastapi import FastAPI
from .settings import settings
from .schemas import HealthResponse

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

@app.get("/health", response_model=HealthResponse, tags=["Monitoring"])
async def health_check():
    return {"status": "ok"}