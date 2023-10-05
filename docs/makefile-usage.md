## Makefile usage documentation
Here is a list of the different possible targets and a brief explanation of what each one does.

* **.venv**: Creates a virtual environment in the project folder. It is not necessary to execute it manually, since it is called by some other target.
* **build-dev**: Builds the docker image for development. It is not necessary to execute it manually, since it is called by some other target.
* **build-test**: Builds the docker image for testing. It is not necessary to execute it manually, since it is called by some other target.
* **clean**: Cleans the project folder of temporary files and folders.
* **delete-containers**: Deletes the containers that are running or that have been stopped. It is not necessary to execute it manually, since it is called by some other target.
* **docs**: Builds the documentation of the project calling the mkdocs command.
* **run**: Runs the docker container for development.
* **run-local**: Runs the project locally. This target calls another target that creates the virtual environment and installs the necessary dependencies, so it is not necessary to do it manually.
* **test**: Runs the docker container for testing.
* **test-local**: Runs the tests locally. This target calls another target that creates the virtual environment and installs the necessary dependencies, so it is not necessary to do it manually.
* **run-precommit**: Runs the pre-commit hooks on the project.
