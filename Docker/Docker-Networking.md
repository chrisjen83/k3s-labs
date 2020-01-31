# Demonstrate Docker Networking

[Return to Main Page](https://github.com/chrisjen83/k3s-labs)

#### Step 1:

Lets start and create a new docker network for this lab called **lab-net**

```
# docker network create lab-net
953f903afdbc05a00db22fa76c5e0cd4b22ac0181fdb52ffde64f057831944a3
```

Lets check we have a new network created. Type the following command.

```
# docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
8b25cde7aa23        bridge              bridge              local
dc12be0dc1e4        host                host                local
953f903afdbc        lab-net             bridge              local
cbc82ac11e3c        none                null                local

```

You will now see your network lab-net, the default bridge network of docker called docker0.  The host network is one which you can attach your containers to to get direct access to your VM machines physical network.

#### Step 2:

We are going to deploy vanilla ubuntu images and access the containers terminal and take a look at how Docker networking functions.  Run the following command to install and setup the first server.

```
# docker run --rm -it --name server1 --net lab-net ubuntu:14.04 bash
```

Once completed you will be automatically placed into that containers command line.

```
root@76793b08141c:/# ls
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@76793b08141c:/# 
```

Now try and ping your server 1 via its hostname which is what you put after --name on your docker run command.  You should be able to ping that server.  Now use the ip address command and inspect your containers network.  The ip address should be coming from the lab-net (Bridge) network 172.18.xx.xx.

#### Step 3:

Lets deploy another docker container, copy the first command you issued to create server1, this time change the name of the container to server2.

Once you are on the command prompt of server 2 try and ping server1 and server2, they should all resolve and ping.

Now we are going to use nc and let you play with sending messages between the two servers.

On server 1 issue the following command:

```
# nc -lp 3456
```

On server 2 type the following command:

```
# nc server1 3456
```

Now you can type abritory messages and they will be sent to the other server.



This lab is to demonstrate that docker has a very simple overlay network which if you assign containers meaning full names allowing container to container communication on the same network is easy.

[Return to Main Page](https://github.com/chrisjen83/k3s-labs)



