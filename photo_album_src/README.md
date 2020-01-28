# Photo Album Source Code

This location hold all of the source code and Dockerfile to modify and create your own version of this website.  It is designed to be made into a Docker Image and deployed on Kubernetes.  The configuration information for the MongoDB Server and S3 buckets are all passed to the Flask Web Server via Kubernetes configMap environment variables.

If you wished to run this image as a docker container within Docker for Desktop there would need to be modifications to the Dockerfile and rebuild the docker image.



_____________________________________________________________________________________________________________________________________________________________________________________________

[Return to Main Page](https://github.com/chrisjen83/k3s-labs)

