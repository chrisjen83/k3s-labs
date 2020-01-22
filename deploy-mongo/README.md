---
typora-copy-images-to: ./
---

# Deploy a Simple MongoDB Server

<img src="/home/christopher/git/k3s-labs/deploy-mongo/MongoDB_Logo_FullColorBlack_RGB-4td3yuxzjs.png" alt="MongoDB_Logo_FullColorBlack_RGB-4td3yuxzjs" style="zoom: 25%;" />

This Lab will step you through the concepts of creating a single MongoDB Database inside a pod on K3s.  This pod will be encapsulated inside a Kubernetes StatefulSet and the database data will be stored on a PVC (Persistent Storage Claim) utilising local k3s storage.

Next you will expose the MongoDB as a headless service (one without external IP address) so that all other pods within your namespace can assess the database via its app name with CoreDNS. You will not be able to access the database externally from the cluster.

<!--Note: if you get errors with kubectl try and use sudo kubectl.-->

To understand the uses and limitations of a StatefulSet use the below link.

[Kubernetes StateFulSets]: https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/

## Step 1:

###### Deploy local storage PVC

```kubectl
kubectl apply -f local-storage-pvc.yaml
```

###### Deploy MongoDB headless service and MongoDB server

We will only be deploying one MongoDB Server within the K3s Cluster. All other students will create their table.

Follow the below commands to deploy and monitor what is happening.

```
kubectl  apply -f mongo-statefulset-v1.yaml
kubectl --namespace default get pods
```

You should notice that the STATUS of the mongo-0 pod is creating.  To understand what is happening in more detail run the below command.

```
kubectl --namespace default describe pods <MONGO_POD_NAME>
```

You will see an output similar to below, the important information at this point is under Events.  Events will tell you step by step what is happening during the deployment of our StatefulSet.

```
Name:         mongo-0
Namespace:    default
Priority:     0
Node:         knode3/192.168.11.23
Start Time:   Thu, 16 Jan 2020 16:48:35 +1100
Labels:       app=mongo-db
              controller-revision-hash=mongo-54d6797944
              environment=test
              role=mongo
              statefulset.kubernetes.io/pod-name=mongo-0
Annotations:  <none>
Status:       Running
IP:           10.42.3.8
IPs:
  IP:           10.42.3.8
Controlled By:  StatefulSet/mongo
Containers:
  mongo:
    Container ID:  containerd://41e3d067995b0e362c5c76c5f12514a953e87b1484770be196ba995a17662c14
    Image:         mongo:4.0.14
    Image ID:      docker.io/library/mongo@sha256:5530a1b06b80de81f294871f40c6fd76d1606165a03c26da418e1ec196af120a
    Port:          27017/TCP
    Host Port:     0/TCP
    Command:
      mongod
      --replSet
      rs0
      --smallfiles
      --noprealloc
      --bind_ip_all
    State:          Running
      Started:      Mon, 20 Jan 2020 18:22:35 +1100
    Last State:     Terminated
      Reason:       Unknown
      Exit Code:    255
      Started:      Thu, 16 Jan 2020 16:48:36 +1100
      Finished:     Mon, 20 Jan 2020 18:22:32 +1100
    Ready:          True
    Restart Count:  1
    Environment:    <none>
    Mounts:
      /data/db from mongo-persistent-storage (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-5bf7l (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
  mongo-persistent-storage:
    Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
    ClaimName:  mongo-persistent-storage-mongo-0
    ReadOnly:   false
  default-token-5bf7l:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-5bf7l
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute for 300s
                 node.kubernetes.io/unreachable:NoExecute for 300s
Events:          <none>

```

Once you have the mongo pod with a STATUS of running proceed to the next step.

[Further reading on StatefulSets](https://github.com/chrisjen83/k3s-labs/tree/master/deploy-metallb)



## Step 2:

###### Initialise the Database.

This section is to demonstrate that we have deployed a docker image and expanded it into a container which is being managed by a Kubernetes Pod.  We are now going to access the container and perform actions as if this was running on our machine.

**exec -it** will start an interactive terminal (-it) running sh command line into the pod then container.

```
kubectl --namespace default get pods
kubectl --namespace default exec -it <POD_NAME> sh
```

Once you have a sh terminal inside the mongoDB Pod log into the mongoDB Server by typing mongo

```
#mongo <ENTER>
```

Once you have logged in you should see the below output, if you do and have a **>** prompt continue to the next step.

```
MongoDB shell version v4.0.14
connecting to: mongodb://127.0.0.1:27017/?gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("5da19fd4-475a-490a-b3b8-56fbef8be7c8") }
MongoDB server version: 4.0.14
Welcome to the MongoDB shell.
For interactive help, type "help".
For more comprehensive documentation, see
	http://docs.mongodb.org/
Questions? Try the support group
	http://groups.google.com/group/mongodb-user
Server has startup warnings: 
2020-01-16T05:48:36.609+0000 I STORAGE  [initandlisten] 
2020-01-16T05:48:36.609+0000 I STORAGE  [initandlisten] ** WARNING: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine
2020-01-16T05:48:36.609+0000 I STORAGE  [initandlisten] **          See http://dochub.mongodb.org/core/prodnotes-filesystem
2020-01-16T05:48:38.833+0000 I CONTROL  [initandlisten] 
2020-01-16T05:48:38.833+0000 I CONTROL  [initandlisten] ** WARNING: Access control is not enabled for the database.
2020-01-16T05:48:38.833+0000 I CONTROL  [initandlisten] **          Read and write access to data and configuration is unrestricted.
2020-01-16T05:48:38.833+0000 I CONTROL  [initandlisten] ** WARNING: You are running this process as the root user, which is not recommended.
2020-01-16T05:48:38.833+0000 I CONTROL  [initandlisten] 
---
Enable MongoDB's free cloud-based monitoring service, which will then receive and display
metrics about your deployment (disk utilization, CPU, operation statistics, etc).

The monitoring data will be available on a MongoDB website with a unique URL accessible to you
and anyone you share the URL with. MongoDB may use this information to make product
improvements and to suggest MongoDB products and deployment options to you.

To enable free monitoring, run the following command: db.enableFreeMonitoring()
To permanently disable this reminder, run the following command: db.disableFreeMonitoring()
---
>
```

Now you need to initialise the database server to be the primary server.

[Further Reading on Mongo Initiate Command]: https://docs.mongodb.com/manual/tutorial/deploy-replica-set/	"Deploy Relica Sets"

```
>rs.initiate()
```

You should see a similar output if initiate is successful.

```
{
	"info2" : "no configuration specified. Using a default configuration for the set",
	"me" : "mongo-0:27017",
	"ok" : 1,
	"operationTime" : Timestamp(1579154177, 1),
	"$clusterTime" : {
		"clusterTime" : Timestamp(1579154177, 1),
		"signature" : {
			"hash" : BinData(0,"AAAAAAAAAAAAAAAAAAAAAAAAAAA="),
			"keyId" : NumberLong(0)
		}
	}
}
rs0:OTHER> 
rs0:PRIMARY>
```

Congratulations you have setup a Mongo Database Server running on Kubernetes inside the default namespace. To exit mongo and the interactive shell follow the below prompts.

```
rs0:PRIMARY> exit
#exit
```