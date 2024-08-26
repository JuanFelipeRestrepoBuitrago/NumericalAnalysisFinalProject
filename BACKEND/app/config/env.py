import os

# Basic configuration
API_NAME = os.getenv('API_NAME')
API_VERSION = os.getenv('API_VERSION')
JWT_SECRET = os.getenv('JWT_SECRET') # The JWT secret string
PRODUCTION_SERVER_URL = os.getenv('PRODUCTION_SERVER_URL')
DEVELOPMENT_SERVER_URL = os.getenv('DEVELOPMENT_SERVER_URL')
LOCALHOST_SERVER_URL = os.getenv('LOCALHOST_SERVER_URL')
