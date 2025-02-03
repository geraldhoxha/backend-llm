MINIKUBEIP:=192.168.49.2

deploy:
	./deploy.sh

serve:
	uvicorn main:app --host 0.0.0.0 --port 8080 --reload

test:
	echo "running tests"
	pytest -s ./tests


dockerbuild:
	./build.sh

# This includes deployment, service, horizontal pod autoscaler (HPA), and the metrics server.
runctl:
	minikube kubectl -- apply -f deploy.yml
	minikube kubectl -- apply -f service.yml
	minikube kubectl -- apply -f hpa.yml
	minikube kubectl -- apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# It sends 25,000 GET requests with a concurrency of 120 and a QPS of 30 to the /health endpoint.
stresstest:
	./hey -n 25000 -c 120 -m GET -q 30 http://$(MINIKUBEIP):30080/health


deletectl:
	minikube kubectl -- delete deploy llm-backend-service
	minikube kubectl -- delete service llm-backend-service
	minikube kubectl -- delete hpa backend-service-hpa

# The 'shutdown' target performs cleanup by:
# 1. Deleting Kubernetes resources in the main directory.
# 2. Changing to the ./llm directory and deleting its Kubernetes resources.
# 3. Resetting the Docker environment to the local Docker daemon.
# 4. Stopping the Minikube cluster.
shutdown: deletectl
	cd ./llm && make deletectl
	cd -
	eval $$(minikube docker-env -u)
	minikube stop
