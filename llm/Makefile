
test:
	pytest -s ./tests/

buildall: startctl dockerbuild runctl

startctl:
	minikube start

dockerbuild:
	./build.sh

runctl:
	minikube kubectl -- apply -f deployment/deploy.yml
	minikube kubectl -- apply -f deployment/service.yml
	minikube kubectl -- apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

deletectl:
	minikube kubectl -- delete deploy llm-model-service
	minikube kubectl -- delete service llm-model-service