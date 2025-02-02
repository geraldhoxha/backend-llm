# LLM Backend

## Installation (Linux)
### Requirements
1. docker
2. minicube
3. hey (stress testing)

#### Doker installation
> [Follow docs.docker.com installation instructions](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

#### Minikube installation
> [Follow minikube.sigs.k8s.io installation instructions](https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download)


#### Hey
Using ```hey``` to test HPA on /health
1. [Download `hey_linux_amd64`](https://hey-release.s3.us-east-2.amazonaws.com/hey_linux_amd64)
2. Move file from downloads to current directory and give exec premision:
    - ```mv ~/Downloads/hey_linux_64 ./hey```
    - ```chmod +x ./hey```

## Run Locally on kubernetes
Simply run ```make deploy```


## Run locally with python
1. Install dependencies
   - ```pip install -r requirements.txt```
2. Run server
   - ```make serve``` 
3. Go to llm/ directory ```cd ./llm``` and run ```make serve```
4. Make sure to change the enpoint in ./routes/client.py to localhost:8081

## Testing
###### Unit tests ```make test```
###### Integration tests ```make integtest```
###### Stress testing ```make stresstest```
Make stresstest will run hey command that will load create **n** requests to the http://\<**url**\>:**30080**/prompt/ endpoint, with the intention of increasing the CPU usage on the pod, thus triggering the autoscaling (HorizontalPodAutoscaler) to deploy an additional deployment to handle the heavy load

