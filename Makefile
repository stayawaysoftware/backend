build:
	sudo docker build --pull --rm -f "Dockerfile" -t demo .

run:
	@sudo docker run -it --name democontainer -p 8000:8000 demo

delete-container:
	@sudo docker stop democontainer
	@sudo docker rm democontainer