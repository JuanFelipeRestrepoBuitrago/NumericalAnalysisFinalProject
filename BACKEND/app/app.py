from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from asyncio import Lock

# Routes and config modules import
from app.api.config.env import API_NAME, PRODUCTION_SERVER_URL, DEVELOPMENT_SERVER_URL, LOCALHOST_SERVER_URL
from app.api.config.limiter import limiter
from app.api.routes.routes import router

from fastapi.openapi.utils import get_openapi


class SynchronousMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.lock = Lock()

    async def dispatch(self, request: Request, call_next):
        async with self.lock:
            response = await call_next(request)
        return response


title = f'{API_NAME} API'
description = f'{API_NAME} API description.'
version = '1.0.0'
servers = [
    {"url": LOCALHOST_SERVER_URL, "description": "Localhost server"},
    {"url": DEVELOPMENT_SERVER_URL, "description": "Development server"},
    {"url": PRODUCTION_SERVER_URL, "description": "Production server"},
]
contact = {
    'name': 'Juan Felipe Restrepo Buitrago',
    'url': 'https://www.eafit.edu.co/',
    'email': 'jfrestrepb@eafit.edu.co',
}
license_info = {
    'name': 'MIT',
    'url': 'https://opensource.org/licenses/MIT',
}


app = FastAPI(
    openapi_url=f'/api/v1/{API_NAME}/openapi.json',
    docs_url=f'/api/v1/{API_NAME}/docs',
    redoc_url=f'/api/v1/{API_NAME}/redoc',
    servers=servers,
    title=title,
    description=description,
    version=version,
    contact=contact,
    license_info=license_info,
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=title,
        version=version,
        description=description,
        routes=app.routes,
        servers=servers,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "..."  # Add your logo URL here
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware configuration
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.add_middleware(SynchronousMiddleware)


@app.on_event('startup')
async def on_startup():
    # Actions to be executed when the API starts.
    print('API started')


@app.on_event('shutdown')
async def on_shutdown():
    # Actions to be executed when the API shuts down.
    print('API shut down')

# Include the routes
app.include_router(router, prefix=f'/api/v1/{API_NAME}')
