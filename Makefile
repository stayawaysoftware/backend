build-dev:
	@sudo docker build --pull --rm -f "Dockerfile.dev" -t dev .

build-test:
	@sudo docker build --pull --rm -f "Dockerfile.test" -t test .

clean:
	@rm -rf */__pycache__ */*/__pycache__ src/*.sqlite

delete-containers:
	@sudo docker stop devcontainer || true && sudo docker rm devcontainer || true
	@sudo docker stop testcontainer || true && sudo docker rm testcontainer || true

mkenv:
	@./configs/setenv.sh
	@pre-commit install

run: delete-containers build-dev
	@sudo docker run -it --name devcontainer -p 8000:8000 dev

run-bash: delete-containers build-dev
	@sudo docker run -it --name devcontainer -p 8000:8000 dev bash

run-local:
	@python3 src/main.py

test: delete-containers build-test
	@sudo docker run -it --name testcontainer -p 8000:8000 test

run-precommit:
	@pre-commit run --all-files
