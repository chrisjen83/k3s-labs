# Setting up MetalLB in K3s

[Return to Main Page](https://github.com/chrisjen83/k3s-labs)

<img src="/home/christopher/Pictures/metallb-logo-5.png" alt="metallb-logo-5" style="zoom: 50%;" />

This tutorial will step you through setting up MetalLB which is a lightweight simple service load balancer for Kubernetes.  To read and the latest information follow this [link](https://metallb.universe.tf/) to the creators web site.

## Step 1:

You will need to deploy MetalLB into the the K3s cluster.  This will be achieved with the below command and this method will be deploying the load balancer from a manifest file.

```kubectl
kubectl apply -f https://raw.githubusercontent.com/google/metallb/v0.8.3/manifests/metallb.yaml
```

> As this tutorial ages it maybe necessary to determine the latest version of MetalLB to deploy.

Once the command has been completed successfully you should have in the **metalld-system** namespace several containers being created as per below.

```
kubectl --namespace metallb-system get pods
NAME                          READY   STATUS    RESTARTS   AGE
speaker-tmg7v                 1/1     Running   1          5d19h
speaker-k8m64                 1/1     Running   1          5d19h
controller-65895b47d4-l6bwc   1/1     Running   1          5d19h
speaker-cwcw9                 1/1     Running   1          5d19h
speaker-qk8rw                 1/1     Running   1          5d19h

```

Once you have your pods looking similar to above it is now time to modify and deploy the configMap for MetalLB.  The configMap will detail the network range of IP addresses which MetalLB will use to hand out to a pod service. Make sure this network is accessible from your machine.

## Step 2:

Open **metallb-config-k3s.yaml** and look at the structure. The most important information is on the last line.  This will declare to MetalLB what address range to give to k3s services when a service deploy file requests  a LoadBalancer.

```
apiVersion: v1
kind: ConfigMap
metadata:
  namespace: metallb-system
  name: config
data:
  config: |
    address-pools:
    - name: default
      protocol: layer2
      addresses:
      - 192.168.11.30-192.168.11.50

```

## Step 3:

Once your **metallb-config-k3s.yaml** is correct for your network it is time to apply the configMap to the metallb deployment.

```
kubectl apply -f metallb-config-k3s.yaml
```

Once the configMap has been applied you have successfully setup MetalLB as a layer 2 load balancer on our K3s Cluster.

[Return to Main Page](https://github.com/chrisjen83/k3s-labs)

