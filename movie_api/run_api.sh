#!/usr/bin/env bash


echo "Waiting for elastic..."

while ! nc -z $ELASTIC_HOST $ELASTIC_PORT; do
    sleep 0.1
done

echo "ElasticSearch started"

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000