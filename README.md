# Muhome 

Music web-blog backend

Works with youtube music API as music base 
to make your posts more filled with related information

## Stack:

- Python
- Django
- Django REST framework
- PostgreSQL
- Docker

## Dependencies

- [docker](https://www.docker.com/)

## Installation

Using [Docker](https://docker.com):

```bash
# build
docker-compose pull
docker-compose build --parallel

# start (will run on http://localhost:8000)
docker-compose up -d

# get logs
docker-compose logs -f backend
docker-compose logs -f

# stop
docker-compose down -t 0

# running backend tests
docker-compose run backend sh -c "PYTHONDONTWRITEBYTECODE=1 ./manage.py test --noinput"
```

## Interfaces to surf API

- [Swagger](http://localhost:8000/api/swagger) | localhost:8000/api/swagger
- [Redoc](http://localhost:8000/api/redoc) | localhost:8000/api/redoc


###### Made with big Love to Music