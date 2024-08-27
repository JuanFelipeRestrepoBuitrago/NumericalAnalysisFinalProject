import os

# Basic configuration
API_NAME = os.getenv('API_NAME')
print('API_NAME:', API_NAME)
API_VERSION = os.getenv('API_VERSION')
print('API_VERSION:', API_VERSION)
JWT_SECRET = os.getenv('JWT_SECRET') # The JWT secret string
print('JWT_SECRET:', JWT_SECRET)
PRODUCTION_SERVER_URL = os.getenv('PRODUCTION_SERVER_URL')
print('PRODUCTION_SERVER_URL:', PRODUCTION_SERVER_URL)
DEVELOPMENT_SERVER_URL = os.getenv('DEVELOPMENT_SERVER_URL')
print('DEVELOPMENT_SERVER_URL:', DEVELOPMENT_SERVER_URL)
LOCALHOST_SERVER_URL = os.getenv('LOCALHOST_SERVER_URL')
print('LOCALHOST_SERVER_URL:', LOCALHOST_SERVER_URL)
