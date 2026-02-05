# Pub-sub Pipeline

## Description:
This is a pub-sub pipeline that scrapes articles from a JSON file and stores them in a MongoDB database.

## How to run:
1. Run `docker-compose up -d --build` to start the containers.
2. Run `docker-compose down -v` to stop the containers.

## How to configure database:
1. Open docker-compose.yml and make sure MongoDB service looks like this:
```
mongo:
  image: mongo:7
  container_name: mongo-pubsub
  ports:
    - "27017:27017"
  environment:
    - MONGO_INITDB_ROOT_USERNAME=main
    - MONGO_INITDB_ROOT_PASSWORD=main123
  restart: unless-stopped
```
2. Set Environment variables for publisher/consumer in docker-compose.yml
3. Start MongoDB container:
```
docker run -d --name mongo-pubsub 
```
4. Verift if the service is running:
```
docker ps
```


## Instructions for running with Docker:
1. Make sure Docker is installed on your system.
2. Run `docker-compose up -d --build` to start the containers.
3. Run `docker-compose down -v` to stop the containers.