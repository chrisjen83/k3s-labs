# Deploy ECS Metadata Search with Docker

[Return to Main Page](https://github.com/chrisjen83/k3s-labs)

This lab will get you to use the docker API to deploy from DockerHub a container image, expand and map to a port number.  You will then be able to access via your Lab VM's local IP Address and the port number the web server.

[Docker Run Additional Reading](https://docs.docker.com/engine/reference/run/)

#### Step 1:

Verify that docker is installed on your Lab VM. You should see something similar to below.

```
# sudo docker version

Client:
 Version:           18.09.9
 API version:       1.39
 Go version:        go1.13.4
 Git commit:        1752eb3
 Built:             Sat Nov 16 01:05:26 2019
 OS/Arch:           linux/amd64
 Experimental:      false

Server:
 Engine:
  Version:          18.09.9
  API version:      1.39 (minimum version 1.12)
  Go version:       go1.13.4
  Git commit:       9552f2b
  Built:            Sat Nov 16 01:07:48 2019
  OS/Arch:          linux/amd64
  Experimental:     false


```

Next we will pull a container image from DockerHub. Use the below command to run the ECS Metadata Search web server

```
# docker run -d --rm -p 5000:5000 chrisjen83/ecs-meta-search:v1
Unable to find image 'chrisjen83/ecs-meta-search:v1' locally
v1: Pulling from chrisjen83/ecs-meta-search
```

You will notice that the docker image **ecs-meta-search:v1** was not found on your local docker registry.  This is normal and expected because the image is on DockerHub and you have never deployed this before.

The docker run command will then by default use docker.io and find the image and pull it into your local registry.

```
8ec398bc0356: Pull complete 
1cfa5cc2566c: Pull complete 
642c5fbdca36: Pull complete 
22c0590866d6: Pull complete 
9cc40ff93d46: Pull complete 
3d0ad18ef397: Pull complete 
Digest: sha256:4fb4b03e33b6baac3c7fede6da004f47c93030a25a12b857c47a36157b1aa615
Status: Downloaded newer image for chrisjen83/ecs-meta-search:v1
975a4f62368f8af9c25f3cea0a05d3facf96948224943a19f7b5a0df70bb8caa
```

By now you should see something similar to above. 

Assume that your docker image is up and running, but lets check this out.

Use the below command to see what is running in Docker.

```
# sudo docker ps
CONTAINER ID        IMAGE                           COMMAND                  CREATED             STATUS              PORTS                    NAMES
975a4f62368f        chrisjen83/ecs-meta-search:v1   "python ecs-meta-sea…"   11 seconds ago      Up 9 seconds        0.0.0.0:5000->5000/tcp   adoring_benz
```

If you see that your docker container is running then everything has worked correctly.  This container run's Python Flask web server.  If python crashed and the flask process stops then this container will stop and be removed.

To access the website open a web browser on your machine and type.

```
http://<LAB VM IP>:5000
```

You should now see the web page asking you to connect to ECS. You have successfully deployed a docker container and have accessed it via its port 5000.

#### Step 2:

Lets now understand what we have done on the command line.

***docker run -it -d --rm -p 5000:5000 chrisjen83/ecs-meta-search:v1*</u>**

**docker run** - This tells the Docker Engine API you want to create a container.

**-d** - this means the container will start in detached mode.  If you started a container in the foreground then your terminal issuing the command would be taken over for the life of the container.

**-p** - This is telling docker to assign port 5000 internally to port 5000 externally.  From a networking point of view all containers running on your VM will have the same external IP address which is your machines hardware IP address.  The way we do network separation externally is port based.

> Note: Docker on Linux will allow you to address from the host OS directly into a containers docker0 network.  For Windows and OS X this is not possible and all interaction with the container has to be via the external IP address of hte host.

**chrisjen83/ecs-meta-search -** this is telling the Docker high level runtime (Containerd) to go to docker.io find the repo chrisjen83 and pull the image ecs-meta-search into your local registry, then unpack and create a local container.

**:v1 -** this is a DockerHub tag which developers can use to version their docker images. If you are unsure of what to use for tags go to DockerHub search for the image and take a look at all of the available tags.

#### Step 3:

Lets now take a look at the docker command ps and understand what we are looking at. Docker ps lets you see all of the running containers in your Docker Engine.

```
# docker ps
```

**CONTAINER ID -** This is a unique alphanumeric name for a container running.  You can use this name with docker commands to inspect or exec into the container.

**STATUS -** If your container failed to start there would be an exit code in this colume to help you troubleshoot. If the container is running correctly it will have the uptime of the container.

**NAME -** if you do not name your container in the docker run API call then Docker Engine will give your container a unique name.  You can also use this name with other docker API commands.

#### Step 4:

Now lets stop run the container and let docker recycle the image.

```
# sudo docker stop <CONTAINER ID OR NAME>
```

If your container has stopped successfully when you do docker ps there should be not running containers listed.

[Next Lab Docker Networking](https://github.com/chrisjen83/k3s-labs/blob/master/Docker/Docker-Networking.md)

[Return to Main Page](https://github.com/chrisjen83/k3s-labs)

