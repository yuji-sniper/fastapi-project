# Docker
up:
	docker-compose up -d

build:
	docker-compose up -d --build

down:
	docker-compose down

prune:
	docker system prune -a --volumes


# コンテナ
app:
	docker-compose exec app /bin/bash

poetry-install:
	docker-compose run --rm app poetry install


# 初回環境構築
init:
	@make build
	@make poetry-install
	@make up
