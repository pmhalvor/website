# build/push/pull the docker images
build:
	docker compose build 

push:
	docker compose push

pull:
	git pull
	docker compose pull

build-push: build push

pull-up: pull up

# run the server
up:
	docker compose up -d

down:
	docker compose down

run: up down

restart: down up
