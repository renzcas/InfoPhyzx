from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infophyz.server.api.routes.cosmos import router as cosmos_router
from infophyz.server.api.routes.math import router as math_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Info-Phys Cosmos Engine",
        description="Backend API for the Info-Phys simulation cockpit",
        version="1.0.0"
    )

    # CORS (frontend → backend)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount routes
    app.include_router(cosmos_router, prefix="/cosmos")
    app.include_router(math_router, prefix="/math")

    return app


app = create_app()


# Optional root route
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Info-Phys Cosmos Engine backend is running"
    }