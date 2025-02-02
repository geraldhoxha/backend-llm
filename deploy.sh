#!/bin/fish

minikube start
eval $(minikube docker-env) && docker build . -t backend-api:v1
eval $(minikube docker-env) && docker build ./llm -t model-api:v1

make runctl
cd ./llm
make runctl

echo "Services started"