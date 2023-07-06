# MovieService

![watchers](https://img.shields.io/github/watchers/dimitrieidifesk/MovieService?style=social)
![forks](https://img.shields.io/github/forks/dimitrieidifesk/MovieService?style=social)
![start](https://img.shields.io/github/stars/dimitrieidifesk/MovieService?style=social)

MovieService - это backend приложения, разработанное на Python, используя микросервисную архитектуру, предназначенное для удобного поиска фильмов и сериалов.
Он осуществляет автоматический сбор данных о кино-новинках, сохраняет их в базу данных PostgreSQL, дает возможность редактировать и данные админкой Django, а затем, с помощью процесса ETL 
(извлечение, преобразование и загрузка), передает данные в Elasticsearch, где можно осуществлять поиск с использованием API на FastAPI.
Удобный запуск Docker

MovieService is a backend application developed in Python using a microservice architecture designed to easily search for movies and series.
It automatically collects movie news data, stores it in a PostgreSQL database, allows editing and data by the Django admin, and then, using the ETL process
(extract, transform and load), passes the data to Elasticsearch, where you can search using the FastAPI API.
Convenient launch with Docker

## Микросервисная архитектура:
![architecture](https://github.com/dimitrieidifesk/MovieService/assets/123076304/04793da4-3707-4599-bddb-a277c96b951e)

## Technologies used in the project

Frameworks:

- FastAPI, Django

Storage:

- PostgreSQL, ElasticSearch, Redis

Containerization

- Docker, Docker-Compose

Web Server/Proxy:

- Gunicorn, Uvicorn, Nginx

- Parsing with a proxy

## installation
Buy proxy addresses and put them in /worker/proxies.txt or don't use proxies

1. Clone the repository:
   
       git clone https://github.com/dimitrieidifesk/MovieService.git
2. Set environment variables:
   
       mv config.env.example config.env
3. Run docker:
   
       docker-compose --env-file config.env up --build


## Useful Commands
1. You may need to collect Django admin static files and put them in nginx_config folder:
   
       python manage.py collectstatic
2. Примените Django миграции:
   
       docker exec -it movieparser-admin_panel-1 python manage.py migrate
