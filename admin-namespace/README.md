# Setup VM and Default Namespace

[Return to Main Page](https://github.com/chrisjen83/k3s-labs)

If you have not already done so, download the VMware image in several 7zip package from this [location](https://github.com/chrisjen83/k3s-labs/tree/master/k8s-vm) and start the image in VMware Workstation/Player/Fusion then login.  Record your IP address so you can ssh into the virtual machine. Your virtual NIC is called **ens33** use the below command to receive your IP address.

```
# ip address
```

For the rest of the labs you will be working in this virtual image.

<!--It is easier to ssh into the image rather than run the command line from within the VMware workstation.-->

## Step 1:

Within your Linux VM lets start by cloning the GitHub repo and get all of the class material you will need.

Follow the below command to clone the repo.

```
# cd ~
# mkdir git
# cd git/
# git clone https://github.com/chrisjen83/k3s-labs.git
```

Inside the **k3s-labs** folder in your git directory go into **admin-namespace** and modify config to represent your student number in the namespace key:value pair **namespace: student<NUMBER>**.

Your file should look similar to below.

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
    password: 
    username: 
```

Now exit and save the file **:wq!**

Next we will need to move config into the correct location for kubectl to access.

Follow the below command.

```
# mv config ~/.kube/config.2
```

## Step 2:

You have been given a local Kubernete's cluster via Microk8s and in this class you will be access the KubePi cluster. To have kubectl access both clusters one at a time it is necessary to modify the context of kubectl.  

To do this you will need to use the below command. 

```
# kubectl config use-context default
```

In the previous step you modified the config to add your student number to the namespace.  If you noticed in the file there was a name given to your context called **default**.  This is the name you used in the above command to set the context to KubePi.  To change back to microk8s use the above command and replace **default** with **microk8s**.

To check if you are looking at KubePi enter the below command.

```
# kubectl config get-contexts
CURRENT   NAME      CLUSTER   AUTHINFO   NAMESPACE
*         default   default   default    student1
```

You should see the **NAMESPACE** will have **student** followed by your student number and the context name is **default**.

You now have access to KubePi API and access to your namespace.  If you want to view all namespaces in the KubePi cluster use the below command.

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