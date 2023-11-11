.venv:
	@python3 -m venv .venv
	@(. .venv/bin/activate; \
	pip install -q -r configs/requirements-dev.txt; \
	pip install -q -r configs/requirements-test.txt; \
	pip install -q -r configs/requirements-utils.txt;)

build-dev:
	@sudo docker build --pull --rm -f "configs/Dockerfile.dev" -t dev .

build-test:
	@sudo docker build --pull --rm -f "configs/Dockerfile.test" -t test .

.PHONY: clean
clean:
	@rm -rf */__pycache__ */*/__pycache__ */*/*/__pycache__ */*/*/*/__pycache__ src/*.sqlite .coverage \
	 */.*_cache coverage.xml .*_cache htmlcov/ site/ .report/

delete-containers:
	@sudo docker stop devcontainer || true && sudo docker rm devcontainer || true
	@sudo docker stop testcontainer || true && sudo docker rm testcontainer || true

.PHONY: docs
docs: .venv
	@(. .venv/bin/activate; \
	mkdocs build -c -f configs/mkdocs.yml; \
	mkdocs serve -f configs/mkdocs.yml)

run: delete-containers build-dev
	@sudo docker run -it --name devcontainer -p 8000:8000 dev

run-local: .venv
	@(. .venv/bin/activate; \
		python3 src/main.py)

test: delete-containers build-test
	@sudo docker run -it --name testcontainer -p 8000:8000 test

test-local: .venv clean
	@(. .venv/bin/activate; \
	pytest -v -s --cov=src --cov-report=term --cov-config=configs/.coveragerc)

test-see-coverage: .venv clean
	@(. .venv/bin/activate; \
	pytest -v -s --cov=src --cov-report=html --cov-config=configs/.coveragerc)
	@xdg-open htmlcov/index.html

run-precommit: .venv clean
	@(. .venv/bin/activate; \
	pre-commit install; \
	pre-commit run --all-files)

report: .venv
	@mkdir -p .report
	@(. .venv/bin/activate; \
	pylint src/ --disable E0401,C0411,C0114,C0115,C0116,E0213 > ./.report/pylint-report; \
	pyflakes src/ > ./.report/pyflakes-report; \
	mypy --ignore-missing-imports src/ > ./.report/mypy-report; \
	vulture src/ > ./.report/vulture-report)
