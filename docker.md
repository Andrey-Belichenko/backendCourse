Docker Network Create
```
docker network crete myNetwork
```
DataBase
```
docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=docker_usr \
    -e POSTGRES_PASSWORD=docker_password \
    -e POSTGRES_DB=booking \
    --network=myNetwork \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16
```
docker run --name booking_db -p 6432:5432 -e POSTGRES_USER=docker_usr -e POSTGRES_PASSWORD=4koifj321poj -e POSTGRES_DB=booking --network=myNetwork --volume pg-booking-data:/var/lib/postgresql/data -d postgres:16

FOR Redis
```
docker run --name booking_cache \
    -p 7379:6379 \
    --network=myNetwork \
    -d redis:7.4
```

docker run --name booking_cache -p 7379:6379 --network=myNetwork -d redis:7.4

OUR CODE 

docker run --name booking_back -p 7777:8000 --network=myNetwork booking_image

Celery

docker run --name booking_celery_worker --network=myNetwork booking_image celery --app=src.tasks.celery_app:celery_instance worker -l INFO

gitlab_with_user



docker build -t booking_image .
