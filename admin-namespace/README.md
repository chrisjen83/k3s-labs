# Configure Default Namespace

[Return to Main Page](https://github.com/chrisjen83/k3s-labs)

To work easily in your student namespace to deploy all of our applications you will need to modify your kubectl config file to add your student namespace as your default namespace.

Lets modify ~/.kube/config with your allocated namespace.

```
# sudo vi ~/.kube/config
```

Now you should see similar below config file.

```
apiVersion: v1
clusters:
- cluster:
    server: https://<IP_ADDRESS>:6443
  name: default
contexts:
- context:
    cluster: default
    namespace: student<NUMBER>
    user: default
  name: default
current-context: default
kind: Config
preferences: {}
users:
- name: default
  user:
    password: 08f4d59abd2d94479e492e36008f8713
    username: admin
```

You will need to modify the namespace value under the **- context** section. Each of you will have been allocated a student number.  Replace <NUMBER> with your allocated number with no spaces.

Save the config file **:wq!** and lets check if this worked.

Enter the below command.

```
#kubectl config get-contexts
CURRENT   NAME      CLUSTER   AUTHINFO   NAMESPACE
*         default   default   default    student1
```

You should see the **NAMESPACE** will have **student** followed by your student number.

To see all of the namespace's on the K3 cluster type.

```
# kubectl get namespaces
NAME              STATUS   AGE
default           Active   5d23h
kube-system       Active   5d23h
kube-public       Active   5d23h
kube-node-lease   Active   5d23h
metallb-system    Active   5d23h
student1          Active   3d2h
student2          Active   29m
student3          Active   29m
student4          Active   29m
student5          Active   29m
student6          Active   29m

```

You should see something similar, every student will be allocated their own namespace to deploy all of the applications into.  MongoDB has been deployed into the **default** namespace and all other namespaces starting with **kube-** are for K3s to use.

If you want to access pods in another namespace append the below to kubectl command:

```
# kubectl --namespace <NAMESPACE_NAME> <COMMAND>

Example:
kubectl --namespace default get pods

NAME      READY   STATUS    RESTARTS   AGE
mongo-0   1/1     Running   1          5d21h

```

[Return to Main Page](https://github.com/chrisjen83/k3s-labs)