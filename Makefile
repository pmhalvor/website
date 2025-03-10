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
build-up: build up

up:
	docker compose up -d

down:
	docker compose down

restart: up

# run the server
run:
	python home/app.py

