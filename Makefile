include .env

ifeq ($(DEV_MODE),true)
    COMPOSE_FILE=dev.yml
else
    COMPOSE_FILE=prod.yml
endif

DC = docker-compose -f $(COMPOSE_FILE) 

auth:
	$(DC) run --rm -it app uv run python get_dialogs.py

ps:
	$(DC) ps -a

logs:
	$(DC) logs -f --tail=1000 app

up:
	$(DC) up -d --build && make logs 

restart:
	$(DC) restart && make logs

stop:
	$(DC) stop

start:
	$(DC) start

db:
	$(DC) exec -it postgres psql -h localhost -U ${DB_USER} -d ${DB_NAME}

migrate:
	$(DC) run --rm app uv run alembic revision --autogenerate

migrateup:
	$(DC) run --rm app uv run alembic upgrade head


