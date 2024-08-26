from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

# Routes and config modules import
from app.api.config.env import API_NAME, PRODUCTION_SERVER_URL, DEVELOPMENT_SERVER_URL, LOCALHOST_SERVER_URL
from app.api.config.limiter import limiter
from app.api.routes.routes import router

from fastapi.openapi.utils import get_openapi

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Actions to be executed during startup
    print('API started')
    
    # Yield control to allow the app to run
    yield
    
    # Actions to be executed during shutdown
    print('API shut down')


title = f'{API_NAME} API'
description = f'{API_NAME} API description.'
version = '0.0.1'
servers = [
    {"url": LOCALHOST_SERVER_URL, "description": "Localhost server"},
    {"url": DEVELOPMENT_SERVER_URL, "description": "Development server"},
    {"url": PRODUCTION_SERVER_URL, "description": "Production server"},
]
contact = {
    'name': 'Juan Felipe Restrepo Buitrago',
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
    lifespan=lifespan
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
        "url": "..." # Add your logo URL here
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

# Include the routes
app.include_router(router, prefix=f'/api/v1/{API_NAME}')