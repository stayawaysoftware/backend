build:
	@sudo docker build --pull --rm -f "Dockerfile.dev" -t demo .

build-test:
	@sudo docker build --pull --rm -f "Dockerfile.test" -t test .

run:
	@sudo docker run -it --name democontainer -p 8000:8000 demo
	@sudo docker stop democontainer
	@sudo docker rm democontainer

test:
	@sudo docker run -it --name democontainer -p 8000:8000 test bash
	@sudo docker stop democontainer
	@sudo docker rm democontainer

run-bash:
	@sudo docker run -it --name democontainer -p 8000:8000 demo bash
	@sudo docker stop democontainer
	@sudo docker rm democontainer

delete-container:
	@sudo docker stop democontainer
	@sudo docker rm democontainer