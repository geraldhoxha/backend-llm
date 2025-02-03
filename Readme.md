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
>  Make a virtual environment ```python3 -m venv .venv``` and ```source .venv/bin/activate```.
> Preferably create a separate virtual environment for **backend** and for **llm**
1. Install dependencies
   - ```pip install -r requirements.txt```
2. Make sure to change the enpoint in ./routes/client.py to localhost:8081
3. Run server
   - ```make serve``` 
4. Go to llm/ directory ```cd ./llm``` and run:
   - ```pip install -r requirements.txt```
5. Run server
   - ```make serve```

# Project structure
```mermaid
graph TD;
   A[Project Root]
   A --> B(main.py)
   A --> C(deploy.sh)
   A --> D(Makefile)
   A --> E(tests/)
   E --> EA(test_client.py)
   A --> F(routers/)
   F --> FA(client.py)
   A --> G(models/)
   G --> GA(models.py)
   A --> H[llm/]
   H --> I(main.py)
   H --> J(Makefile)
   H --> K(tests/)
   K --> KA(tests/)
   KA --> KB(test_model.py)
   H --> L(routes/)
   L --> LA(endpoint.py)
   H --> M(model/)
   M --> MA(model.py)

```
# Architecture overview
```mermaid
flowchart TD
   A[Client/Frontend]
   subgraph K[Kubernetes Cluster]
      B[Backend Service]
      subgraph LLM_Services [LLM Services]
         C1[LLM Instance 1]
         C2[LLM Instance 2]
         C3[LLM Instance N]
      end
   end

   %% Request flow
   A -->|HTTP Request| B
   B -->|Forward Prompt| C1
   B -->|Forward Prompt| C2
   B -->|Forward Prompt| C3

   %% Response flow (from any scaled LLM instance back to Backend)
   C1 -->|Generate Image| B
   C2 -->|Chat Conversation| B
   C3 -->|Does something| B
   B -->|HTTP Response| A

```
Backend service will handle all requests which will forward the prompts to the service. Scales horizontally with minimal CPU & MEM usage.
Each LLM service runs independently from each other and scales vertically.

# Generate image using terminal
```curl
curl --header "Content-Type: application/json" \
 --request POST \
 --data '{"text": "**PROOMPT HERE**"}' \
 http://MinikubeIP:30081/model/generate \
 --output response.png
```

## Testing
###### Unit tests ```make test```
###### Stress testing ```make stresstest```
Make stresstest will run hey command that will create **n** requests to the http://\<**url**\>:**30080**/health/ endpoint, with the intention of increasing the CPU usage on the pod, thus triggering the autoscaling (HorizontalPodAutoscaler) to deploy an additional deployment to handle the heavy load

