# Deploy a Photo Album web page

[Return to Main Page](https://github.com/chrisjen83/k3s-labs)

<img src="1200px-Flask_logo.svg.png" alt="1200px-Flask_logo.svg" style="zoom:50%;" />

This lab will get you to deploy a basic Python Flask web server which will connect to a MongoDB Database which was setup in the [previous lab](https://github.com/chrisjen83/k3s-labs/tree/master/deploy-mongo#setup-mongodb-on-k3s-arm64). Most of the web sites coding is done for you but you will need to enter your database table name and ECS Test Drive S3 API credentials into a Kubernetes configMap file.

## Step 1:

You will need to create a database table in the MongoDB server which was previously deployed.  Lets log into MongoDB Pod via an interactive shell.

```
# kubectl --namespace default get pods
# kubectl --namespace default exec -it <MONGODB_POD_NAME> sh
```

Once you have a sh terminal inside the mongoDB Pod log into the mongoDB Server by typing mongo

```
# mongo <ENTER>
```

Once you have a **>** prompt type the following command to create a table to use with your web site. Replace <TABLE_NAME> with a name you wish to use appended with your student number at the end.

```
rs0:PRIMARY> use <TABLE_NAME>
switched to db <TABLE_NAME>
rs0:PRIMARY> exit
bye
# exit
```

Write down or remember your table name as this information will need to be use later in this lab.

## Step 2:

To deploy your web page application there are several components that need to be configured in order for your application to function correctly.

- [ ] **configMap** created with your MongoDB Table name, ECS Test Drive creidentuals and MongoDB Server address.  Your pod will advertise enviroment variables to the container which flask will read.
- [ ] **Service (LoadBalancer)** is need to be linked to your web page pod to expose Flasks port 5000 externally of the K3s cluster and assign an external IP address. If this was not created you could not access the web page on your computer.
- [ ] **Deployment** which will define the desired state of your web server, link it to the Service and import the enviroment variables from the configMap.

Use **k3s-photo-album-deploy-v4.yaml** located in deploy-photo-album folder, this YAML has all of the needed components listed above in the one file.  Kubernetes will read this file and configure your configMap, Service and Deploy your pod.

Lets get started, in the below code snippet when I use **< .. >** this means you will need to configure these settings with your details.

```
kind: ConfigMap
apiVersion: v1
metadata:
  name: photo-album-configmap
  namespace: <INSERT_YOUR_NAMESPACE_NAME>
data:
  DB_NAME: <CREATED_DB_ABLE_NAME>
  MONGO_SERVER: mongodb://<POD_NAME>.<NAMESPACE>.svc.cluster.local:27017
  ecs_endpoint_url: https://object.ecstestdrive.com
  ecs_access_key_id: <YOUR_S3_ACCESS_KEY>
  ecs_secret_key: <YOUR_S3_SECRET>
  ecs_bucket_name: <BUCKET_NAME>
```

```
apiVersion: v1
kind: Service
metadata:
  name: photo-album
  namespace: <INSERT_YOUR_NAMESPACE_NAME>
  labels:
    app: <APPLICATION_NAME>
    spec:
  type: LoadBalancer
  ports:
  - port: 5000
  selector:
    app: <APPLICATION_NAME>
```

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: photo-album
  namespace: <INSERT_YOUR_NAMESPACE_NAME>
  labels:
    app: <APPLICATION_NAME>
```

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: photo-album
  namespace: <INSERT_YOUR_NAMESPACE_NAME>
  labels:
    app: <APPLICATION_NAME>
spec:
  replicas: 1
  selector:
    matchLabels:
      app: <APPLICATION_NAME>
  template:
    metadata:
      labels:
        app: <APPLICATION_NAME>
    spec:
      containers:
      - name: photo-album
        image: chrisjen83/photo_album-arch:v4
        imagePullPolicy: Always
        envFrom:
          - configMapRef:
              name: photo-album-configmap
        ports:
        - containerPort: 5000
```



## Step 3:

Now it is time to deploy **k3s-photo-album-deploy-v4.yaml** into your namespace and let the magic happen.

```
# ckubectl apply -f k3s-photo-album-deploy-v4.yaml
```

Once this has executed successfully lets take a look at what Kubernetes is doing.

First lets see if Kubernetes has created a pod, to do this issue the following command.

```
# kubectl  get pods
```

Your output should look similar to below, take a look at the STATUS column.  This will tell you what is happening inside the pod.

```
NAME                           READY   STATUS    RESTARTS   AGE
mongo-0                        1/1     Running   0          23h
photo-album-6dfdfb6597-cpfxk   1/1     Running   0          23h
```

But to really understand what is happening we need to describe the pod, so lets do that.

```
# kubectl describe pods <PHOTO-ALBUM_POD_NAME>
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

Lets take a look at that service we created inside our deployment YAML.  Type the below command to find out.

```
# kubectl get svc
```

```
NAME          TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)          AGE
photo-album   LoadBalancer   10.43.134.178   192.168.11.30   5000:31604/TCP   25h

```

Look for the line which has the name of your app you deployed.  You will notice that the service **TYPE** is LoadBalancer and the **EXTERNAL-IP** is an address on the 192.168.11.x/24 network and the PORT is 5000.

Great lets load this web page from your laptop and start uploading photo's to your album.  Your address will be http://192.168.11.x:5000

[Return to Main Page](https://github.com/chrisjen83/k3s-labs)