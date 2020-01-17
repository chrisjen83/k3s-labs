# Deploy a Photo Album web page on K3s

This lab will introduce the concepts of pods, container images from a remote registry (DockerHub), S3 non-persistent storage, and Kubernetes networking. Your web page will be connecting to ECS S3 storage to upload all of your full size photo's and thumbnails. MongoDB will hold a reference to all images and store the titles and comments.

This lab will get you to deploy a basic Python Flask web server which will connect to your MongoDB Database you setup on the [previous lab](https://github.com/chrisjen83/k3s-labs/tree/master/deploy-mongo#setup-mongodb-on-k3s-arm64). Most of the web sites coding is done for you and all database connections are pre-entered.  You must have completed the previous lab and created a database called **mongodb**, the naming of the database is critical.

> If you spelt or wrote the name of the database wrong the web page will fail to load with error "Internal Server Error".  If you look at the Flask logs in Kubernetes you will see error connecting to the database.

## Step 1:

You will need to use **k3s-photo-album-deploy-v2.yaml**, this is an application deployment file for Kubernetes.  This yaml file will download the docker image photo_album-arch:v2 from DockerHub and create a container with in a pod called photo-album.  This this deployment we will create a service which will expose the flask web server out to the world through a load balancer inside of Kubernetes.

Lets get started...

As you did in the [previous lab](https://github.com/chrisjen83/k3s-labs/tree/master/deploy-mongo#setup-mongodb-on-k3s-arm64) you will need to edit **k3s-photo-album-deploy-v2.yaml** and include the namespace corresponding to your allocated namespace for both the service and the deployment.

```
apiVersion: v1
kind: Service
metadata:
  name: photo-album
  namespace: <INSERT_YOUR_NAMESPACE_NAME>
  labels:
    app: album
```

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: photo-album
  namespace: <INSERT_YOUR_NAMESPACE_NAME>
  labels:
    app: album
```

## Step 2:

Now it is time to deploy **k3s-photo-album-deploy-v2.yaml** into your namespace and let the magic happen.

```
kubectl --namespace <YOUR_NAMESPACE> apply -f k3s-photo-album-deploy-v2.yaml
```

Once this has executed successfully lets take a look at what Kubernetes is doing.

First lets see if Kubernetes has created a pod, to do this issue the following command.

```
kubectl --namespace <YOUR_NAMESPACE> get pods
```

Your output should look similar to below, take a look at the STATUS column.  This will tell you what is happening inside the pod.

```
NAME                           READY   STATUS    RESTARTS   AGE
mongo-0                        1/1     Running   0          23h
photo-album-6dfdfb6597-cpfxk   1/1     Running   0          23h
```

But to really understand what is happening we need to describe the pod, so lets do that.

```
kubectl --namespace <YOUR_NAMESPACE> describe pods <PHOTO-ALBUM_POD_NAME>
```

 You will receive an output similar to below.

```
Name:         photo-album-6dfdfb6597-p6rbx
Namespace:    default
Priority:     0
Node:         knode1/192.168.11.21
Start Time:   Fri, 17 Jan 2020 16:40:32 +1100
Labels:       app=album
              pod-template-hash=6dfdfb6597
Annotations:  <none>
Status:       Running
IP:           10.42.1.12
IPs:
  IP:           10.42.1.12
Controlled By:  ReplicaSet/photo-album-6dfdfb6597
Containers:
  photo-album:
    Container ID:   containerd://c2d3c718d10259ba26df5108fa6b9f9836a64f8bda6dbf2ec9ce7896a2530fa7
    Image:          chrisjen83/photo_album-arch:v2
    Image ID:       docker.io/chrisjen83/photo_album-arch@sha256:6f9d6fb7a14c40e726f8eca66236766e1e9967e7692bfa56da0928598c8aa7cc
    Port:           5000/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Fri, 17 Jan 2020 16:40:36 +1100
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-5bf7l (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
  default-token-5bf7l:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-5bf7l
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute for 300s
                 node.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type    Reason     Age        From               Message
  ----    ------     ----       ----               -------
  Normal  Scheduled  <unknown>  default-scheduler  Successfully assigned default/photo-album-6dfdfb6597-p6rbx to knode1
  Normal  Pulling    26s        kubelet, knode1    Pulling image "chrisjen83/photo_album-arch:v2"
  Normal  Pulled     23s        kubelet, knode1    Successfully pulled image "chrisjen83/photo_album-arch:v2"
  Normal  Created    23s        kubelet, knode1    Created container photo-album
  Normal  Started    23s        kubelet, knode1    Started container photo-album
```

In the above output you should look at the Event section at the bottom, this is telling you what is happening to create the pod and create the container with our web page photo album.

If there are any errors pulling the image or starting the pod the Event section will tell you what is happening.

At this point I am assuming your pod has started, now you might ask what is the IP address to access this web page? 

Lets take a look at that Service we created inside our deployment YAML.  Type the below command to find out.

```
kubectl --namespace <YOUR_NAMESPACE> get svc
```

```
NAME          TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)          AGE
kubernetes    ClusterIP      10.43.0.1       <none>          443/TCP          26h
mongo         ClusterIP      None            <none>          27017/TCP        26h
photo-album   LoadBalancer   10.43.134.178   192.168.11.30   5000:31604/TCP   25h

```

Look for the line which has the name of your app you deployed photo-album.  You will notice that the service **TYPE** is LoadBalancer and the **EXTERNAL-IP** is an address on the 192.168.11.x/24 network and the PORT is 5000.

Great lets load this web page from your laptop and start uploading photo's to your album.

