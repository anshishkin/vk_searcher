SHELL = /bin/sh
CURRENT_UID := $(shell id -u)

build:
	DOCKER_BUILDKIT=1 docker-compose build

rebuild:
	DOCKER_BUILDKIT=1 docker-compose build --no-cache

format:
	docker run --rm -v $(CURDIR):/data --workdir /data pyfound/black black . -l 120 -t py38

fixperm:
	sudo chown -R $(CURRENT_UID) ./

down:
	docker-compose down