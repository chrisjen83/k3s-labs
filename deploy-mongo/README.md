# Setup MongoDB on K3s ARM64

This Lab will step you through the concepts of creating a single MongoDB Database inside a pod.  This pod will be encapsulated inside of a Kubernetes StatefulSet and the database data will be stored on a persistent storage provider in a PVC (Persistent Storage Claim).

Next you will expose the MongoDB as a headless service (one without external IP address) so that all other pods within your namespace can assess the database via its app name with CoreDNS.

Go ahead and pull this repo onto your machine, it will include all of the Kubernetes deploy files needed.

<!--Note: if you get errors with kubectl try and use sudo kubectl.-->

To understand the uses and limitations of a StatefulSet use the below link.

[]: https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/

## Step 1:

###### Deploy local storage PVC

```kubectl
kubectl --namespace <YOUR_NAMESPACE> apply -f local-storage-pvc.yaml
```

###### Deploy MongoDB headless service and MongoDB server

Before you deploy this yaml file you need to modify ***mongo-statefulset-v1.yaml*** to reference your namespace correctly.

Modify the Service section:

```
apiVersion: v1
kind: Service
metadata:
  name: mongo
  namespace: <INSERT_YOUR_NAMESPACE_NAME>
  labels:
    name: mongo
```

Modify the StatefulSet:

```
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mongo
  namespace: <INSERT_YOUR_NAMESPACE_NAME>
```

Now save your yaml file and deploy it into the Kubernetes Cluster. Once the StatefulSet has applied without error, use kubectl to verify the pod is being created.

```
kubectl --namespace <YOUR_NAMESPACE> apply -f mongo-statefulset-v1.yaml
kubectl --namespace <YOUR_NAMESPACE> get pods
```

[Further reading on StatefulSets]: https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/	"StatefulSets"



## Step 2:

###### Initialise the Database.

This section is to demonstrate that we have just deployed a docker image and expanded it into a container which is being managed by a Kubernetes Pod.  We are now going to access the container and perform actions as if this was running on our machine.

**exec -it** will start an interactive terminal (-it) running sh command line into the pod then container.

```
kubectl --namespace <YOUR_NAMESPACE> get pods
kubectl --namespace <YOUR_NAMESPACE> exec -it <POD_NAME> -- sh
```

Once you have a sh terminal inside the mongoDB Pod log into the mongoDB Server by typing mongo

```
#mongo <ENTER>
```

Once you have logged in you should see the below output, if you do and have a > prompt continue to the next step.

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



Next create the database for the photo album website called **mongodb** then exit the mongo command prompt and then exit the exec session into the Pod and return to your local command prompt.

```
rs0:PRIMARY> use mongodb
rs0:PRIMARY> exit
#exit
```

Congratulations you have completed the MongoDB setup, please proceed to the next tutorial.