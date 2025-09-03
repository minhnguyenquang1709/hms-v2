from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from fastapi.openapi.docs import get_swagger_ui_html
from .api import api_router
from .config.db import config, get_db, session_manager
import logging
from dotenv import load_dotenv

load_dotenv()

EXPOSE_PORT = int(os.getenv("EXPOSE_PORT", 4000))

logger = logging.getLogger(__name__)


def init_app(init_db: bool = True):
    lifespan = None  # type: ignore
    if init_db:
        session_manager.init(config.DB_CONFIG)

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            """
            Application lifespan context manager for FastAPI.
            This is used to manage startup and shutdown events.
            """
            try:
                session_manager.init(config.DB_CONFIG)
                async with session_manager.connect() as conn:
                    await session_manager.create_all(conn)
                logger.info("Database session manager initialized")
            except Exception as e:
                logger.critical(
                    f"Failed to initialize database session manager: {str(e)}"
                )
                raise
            yield
            # add cleanup code when the app shuts down.
            if session_manager._engine:
                await session_manager.close()

    server = FastAPI(lifespan=lifespan, title="HIS")
    return server


app = init_app()

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

favicon_path = "hospital.png"


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    """
    Serve the favicon for the application.
    """
    from fastapi.responses import FileResponse

    return FileResponse(favicon_path)


# @app.get("/docs", include_in_schema=False)
# def overriden_swagger():
#     return get_swagger_ui_html(
#         openapi_url=app.openapi_url if app.openapi_url else "/openapi.json",
#         title=app.title + " - Swagger UI",
#         swagger_favicon_url=favicon_path,
#     )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="src.main:app", host="0.0.0.0", port=EXPOSE_PORT, reload=True)
