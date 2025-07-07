from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager for FastAPI.
    This is used to manage startup and shutdown events.
    """
    yield
    # Here you can add any cleanup code if needed when the app shuts down.


app = FastAPI(lifespan=lifespan)

# middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
