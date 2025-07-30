from fastapi import FastAPI
from ..utils.config import Config

def create_app(config: Config) -> FastAPI:
    app = FastAPI(
        title="OpenRXN Perovskite Optimizer API",
        description="API for the OpenRXN Perovskite Optimizer",
        version="1.0.0",
    )

    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    return app