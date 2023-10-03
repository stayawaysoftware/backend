## Guide to run the project
There are 2 different ways to run it, each with its own utility.

One is the local way as we would conventionally do it and the other is containerized by raising an instance of a custom docker image.

### Running it locally
For this we use a venv virtual environment which is self-configured using a Makefile target.
Before we start we must have venv installed on our computer and of course python 3.x.

If you don't have venv installed you can install it by running:
```apt install python3-venv```

After that we will run the autoconfiguration using the Makefile:
```make mkenv```

At the end of this task we have our environment configured and it is enough to activate it when we want to use it and deactivate it when we don't want to use it anymore.

To activate it, inside the src directory, we execute:
```source venv/bin/activate```

Now we can run the code locally with the makefile target:
```make run-local```

Then to deactivate it we only execute:
```deactivate```


### Running it containerized
For ease of use there are makefile targets that allow us to make it easy to use. But before using it, docker must be installed as the only dependency.

To install it on debian/ubuntu based you can run:
```sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin```

To see the different execution possibilities see the [makefile-usage](makefile-usage.md) file, but normally you will want to execute:
```make run``` which normally runs the project but in a containerized way.
