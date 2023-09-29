## Makefile usage documentation
Here is a list of the different possible targets and a brief explanation of what each one does.


* **build-dev**: Creates the docker image required for the development environment. Normally it is not executed manually, but is called by some other run target.
* **build-test**: Same as the previous build but for the testing environment.
* **mkenv**: Create the local environment to be able to execute the code locally.
* **run**: Remove the necessary containers if they are running, build the image and run a container executing the main of the code, thus raising an instance of the server.
* **run-bash**: It does the same as the previous one, but it does not automatically run the server instance but it opens a bash to interact (if desired) with the system that hosts the docker instance.
* **run-local**: Execute the code locally
* **test**: It performs the same actions as in the run, except that it executes the tests instead of raising an instance of the server.
* **delete-containers**: It eliminates the containers that we may have used and were left running in the background.
* **clean**: Removes certain unneeded files that are the result of local code execution.
