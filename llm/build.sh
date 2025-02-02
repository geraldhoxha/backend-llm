#!/bin/fish

echo "Building docker image using Fish"

eval $(minikube docker-env) && docker build . -t model-api:v1
