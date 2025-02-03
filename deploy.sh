#!/bin/fish

# Start minikube cluster
minikube start

# Set minikube's deamon claster and build docker images
eval $(minikube docker-env) && docker build . -t backend-api:v1
eval $(minikube docker-env) && docker build ./llm -t model-api:v1

# Run kubernetes files
make runctl
cd ./llm
make runctl

echo "Services started"