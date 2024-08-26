import os

# Basic configuration
API_NAME = os.getenv('API_NAME') | 'backend_numerical_methods'
API_VERSION = os.getenv('API_VERSION') | 'v0.0.1'
JWT_SECRET = os.getenv('JWT_SECRET') | 'Hola' # The JWT secret string
PRODUCTION_SERVER_URL = os.getenv('PRODUCTION_SERVER_URL') | 'http://localhost:8000/'
DEVELOPMENT_SERVER_URL = os.getenv('DEVELOPMENT_SERVER_URL') | 'http://localhost:8000/'
LOCALHOST_SERVER_URL = os.getenv('LOCALHOST_SERVER_URL') | 'http://localhost:8000/'
