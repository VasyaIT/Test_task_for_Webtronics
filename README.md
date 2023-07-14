# Test_task_for_Webtronics
Simple RESTful API using FastAPI for a social networking application

## Before start, set your settings in the .env file
```
SECRET_KEY=''  # random key

TOKEN_AUDIENCE=''  # example jwt

POSTGRES_ENGINE=postgresql
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD='' db password

DB_ENGINE_TEST=''  # test engine db
DB_HOST_TEST=''  # test db host
DB_PORT_TEST=''  # test db port
DB_NAME_TEST=''  # test db name
DB_USER_TEST=''  # test db user
DB_PASSWORD_TEST=''  # test db password

REDIS_HOST=redis
REDIS_PORT=6379 

CORS_ORIGIN=http://localhost:8000  # and your
```
# Very important!
+ **If the project does not up the first time, try again or delete the 'data' folder!**  
# Start
```commandline
docker compose up --build
```
# Tests
```commandline
docker compose exec web pytest tests
```
