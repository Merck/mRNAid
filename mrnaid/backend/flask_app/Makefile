ENV_NAME := mRNAid
SHELL := /bin/bash
CONDA_ACTIVATE = eval "$$(conda shell.bash hook)" && conda activate $(ENV_NAME)
REDIS_VERSION := 6.0.9

env-create: 
	conda env update --name $(ENV_NAME) --file environment.yml

redis-install:
	wget https://download.redis.io/releases/redis-$(REDIS_VERSION).tar.gz; \
	tar xzf redis-$(REDIS_VERSION).tar.gz; \
	cd redis-$(REDIS_VERSION); \
	make;

redis-run:
	$(CONDA_ACTIVATE); \
		redis-$(REDIS_VERSION)/src/redis-server

uwsgi-run:
	$(CONDA_ACTIVATE); \
		APP_NAME=backend \
		CELERY_BROKER_URL=redis://127.0.0.1:6379 \
		CELERY_RESULT_BACKEND=redis://127.0.0.1:6379 \
		LOG_FILE=./logs/logs.log \
		BACKEND_OBJECTIVES_DATA=../common/objectives/data \
		PYTHONPATH=../common:../common/objectives:../common/constraints\
		uwsgi --ini app.ini:uwsgi-no-docker

celery-run:
	$(CONDA_ACTIVATE); \
		CELERY_BROKER_URL=redis://127.0.0.1:6379 \
		CELERY_RESULT_BACKEND=redis://127.0.0.1:6379 \
		LOG_FILE=./logs/logs.log \
		BACKEND_OBJECTIVES_DATA=../common/objectives/data \
		PYTHONPATH=../common:../common/objectives:../common/constraints\
		celery -A tasks worker --loglevel=info

flower-run:
	$(CONDA_ACTIVATE); \
		CELERY_BROKER_URL=redis://127.0.0.1:6379 \
		CELERY_RESULT_BACKEND=redis://127.0.0.1:6379 \
        celery flower --port=5566