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

change directory into k3s-labs/ecs_meta_search/instance, in this directory will be application-cfg-map.yml.

Lets apply this into your namespace.

```
# kubectl create -f application-cfg-map.yml
```







[Return to Main Page](https://github.com/chrisjen83/k3s-labs)