from os import environ

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = environ.get('SECRET_KEY')

# Database
DB_ENGINE = environ.get('DB_ENGINE')
DB_HOST = environ.get('DB_HOST')
DB_PORT = environ.get('DB_PORT')
DB_NAME = environ.get('DB_NAME')
DB_USER = environ.get('DB_USER')
DB_PASSWORD = environ.get('DB_PASSWORD')

# Test database
DB_ENGINE_TEST = environ.get('DB_ENGINE_TEST')
DB_HOST_TEST = environ.get("DB_HOST_TEST")
DB_PORT_TEST = environ.get("DB_PORT_TEST")
DB_NAME_TEST = environ.get("DB_NAME_TEST")
DB_USER_TEST = environ.get("DB_USER_TEST")
DB_PASSWORD_TEST = environ.get("DB_PASSWORD_TEST")

# Auth
JWT_LIFETIME = 10 * 60
COOKIE_NAME = 'JWT'
TOKEN_AUDIENCE = environ.get('TOKEN_AUDIENCE')

# REDIS
REDIS_HOST = environ.get('REDIS_HOST')
REDIS_PORT = environ.get('REDIS_PORT')

# CORS
CORS_ORIGIN = environ.get('CORS_ORIGIN').split(' ')
ALLOW_METHODS = ["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"]
ALLOW_HEADERS = ["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                 "Access-Control-Allow-Origin", "Authorization"]
