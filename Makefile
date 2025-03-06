# build/push/pull the docker images
build:
	docker compose build 

push:
	docker compose push

pull:
	docker compose pull

build-push: build push

# run the server
up:
	docker compose up --build

down:
	docker compose down

run: up down

restart: down up

