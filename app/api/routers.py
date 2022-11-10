from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.endpoints import query, auth, device_management


def execute():
    fastAPI = FastAPI()
    origins = [
       '*'
    ]

    fastAPI.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    fastAPI.include_router(auth.router, prefix="/api")
    fastAPI.include_router(query.router, prefix="/api")
    fastAPI.include_router(device_management.router, prefix="/api/device")
    return fastAPI
