## Guide to run the project
There are 2 different ways to run it, each with its own utility.

One is the local way as we would conventionally do it and the other is containerized by raising an instance of a custom docker image.

### Running it locally
For this we use a venv virtual environment which is self-configured using a Makefile target.
Before we start we must have venv installed on our computer and of course python 3.x.

If you don't have venv installed you can install it by running:
```apt install python3-venv```

Now we can run the code locally with the makefile target:
```make run-local```

This target call to another target that creates the virtual environment and installs the necessary dependencies, so it is not necessary to do it manually.


### Running it containerized
For ease of use there are makefile targets that allow us to make it easy to use. But before using it, docker must be installed as the only dependency.

To install it on debian/ubuntu based you can run:
```sudo apt-get install docker*```

To see the different execution possibilities see the [makefile-usage](makefile-usage.md) file, but normally you will want to execute:
```make run``` which normally runs the project but in a containerized way.
