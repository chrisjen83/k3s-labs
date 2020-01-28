# Deploy ECS Metadata Search Application
[Return to Main Page](https://github.com/chrisjen83/k3s-labs)

In this lab we will be deploying a web site which is connecting to a Dell EMC ECS object storage system.  This GUI is taking ECS S3 metasearch API and putting it into a easy to use GUI.

This lab will demonstrate basic pod and container image deployment on kubernetes and how object storage can be assessed via API from within a Pod.

## Step 1:

Change directory into k3s-labs/ecs_meta_search/deploy  In this directory there will be deployment.yaml.  This is the combined deployment file that will create a LoadBalancer Service and a web server hosting the GUI.  Lets apply this into your namespace.

```
# kubectl create -f deployment.yaml
```

Next you will need to create a configMap so that the web server can connect to the ECS instance hosting a Metadata Search bucket.

Change directory into k3s-labs/ecs_meta_search/instance, in this directory will be application-cfg-map.yml.

Lets apply this into your namespace.

```
# kubectl create -f application-cfg-map.yml
```

## Step 2:

Now that you have the application deployed with its configurations, lets access the website.

First you will need to see what IP address the Load Balancer service has given to your deployment. Perform the following command.

```
# kubectl get svc
NAME                      TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)          AGE
photo-album               LoadBalancer   10.43.138.146   192.168.11.30   5000:31166/TCP   5d19h
ecs-meta-search-service   LoadBalancer   10.43.194.37    192.168.11.31   5000:30369/TCP   5d19h
```

Please take note of your ecs-meta-search-service **EXTERNAL-IP**.  This is what you will use from your laptop to access the website.

On your laptop open a web browser and enter http://192.168.11.xx:5000 

You should now see the website and an ECS Metadata Search GUI.

Have a play with the search function try and use **source** and search for **shutterstock**.  You should get a list of several video's which you can click on the download link and watch.

All of this GUI functionality is coming from the ECS metadata search API and the playing of the footage is streaming straight out of an ECS bucket.

[Return to Main Page](https://github.com/chrisjen83/k3s-labs)