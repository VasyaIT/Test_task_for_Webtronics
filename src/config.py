from os import environ

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = environ.get('SECRET_KEY', 'weffhwieugf@H#I2jrT$#tjheorhgeiurghierhgg54##R$%Tgreg')

# Database
DB_ENGINE = environ.get('POSTGRES_ENGINE', 'postgresql')
DB_HOST = environ.get('POSTGRES_HOST', 'db')
DB_PORT = environ.get('POSTGRES_PORT', 5432)
DB_NAME = environ.get('POSTGRES_NAME', 'postgres')
DB_USER = environ.get('POSTGRES_USER', 'postgres')
DB_PASSWORD = environ.get('POSTGRES_PASSWORD', '123456')

# Test database
DB_ENGINE_TEST = environ.get('DB_ENGINE_TEST', 'postgresql')
DB_HOST_TEST = environ.get("DB_HOST_TEST", 'db')
DB_PORT_TEST = environ.get("DB_PORT_TEST", 5432)
DB_NAME_TEST = environ.get("DB_NAME_TEST", 'postgres')
DB_USER_TEST = environ.get("DB_USER_TEST", 'postgres')
DB_PASSWORD_TEST = environ.get("DB_PASSWORD_TEST", '123456')

# Auth
JWT_LIFETIME = 10 * 60
COOKIE_NAME = 'JWT'
TOKEN_AUDIENCE = environ.get('TOKEN_AUDIENCE', 'jwt')

# REDIS
REDIS_HOST = environ.get('REDIS_HOST', 'redis')
REDIS_PORT = environ.get('REDIS_PORT', 6379)

# CORS
CORS_ORIGIN = environ.get('CORS_ORIGIN', 'http://localhost:8000').split(' ')
ALLOW_METHODS = ["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"]
ALLOW_HEADERS = ["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                 "Access-Control-Allow-Origin", "Authorization"]
