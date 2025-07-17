from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager for FastAPI.
    This is used to manage startup and shutdown events.
    """
    yield
    # Here you can add any cleanup code if needed when the app shuts down.


app = FastAPI(lifespan=lifespan)

# middleware config
origins = ["*"]
methods = ["*"]
headers = ["*"]

# middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=methods,
    allow_headers=headers,
    allow_credentials=True,
)

app.include_router(api_router)