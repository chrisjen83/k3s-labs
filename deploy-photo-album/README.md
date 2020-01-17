# Deploy a Photo Album Webpage on K3s

This lab will introduce the concepts of pods, container images from a remote registry (DockerHub), S3 non-persistent storage, and Kubernetes networking. Your web page will be connecting to ECS S3 storage to upload all of your full size photo's and thumbnails. MongoDB will hold a reference to all images and store the titles and comments.

This lab will get you to deploy a basic Python Flask web server which will connect to your MongoDB Database you setup on the [previous lab](https://github.com/chrisjen83/k3s-labs/tree/master/deploy-mongo#setup-mongodb-on-k3s-arm64). Most of the web sites coding is done for you and all database connections are pre-entered.  You must have completed the previous lab and created a database called **mongodb**, the naming of the database is critical.

> If you spelt or wrote the name of the database wrong the webpage will fail to load with error "Internal Server Error".  If you look at the Flask logs in Kubernetes you will see error connecting to the database.

## Step 1:

