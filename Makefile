MINIKUBEIP:=192.168.49.2
serve:
	uvicorn main:app --host 0.0.0.0 --port 8080 --reload

test:
	echo "running unit tests"
	pytest tests/unit/

integtest:
	echo "running integration tests"
	pytest tests/integration/

validate:
	echo "running all tests"
	pytest tests/

buildall: startctl dockerbuild runctl

startctl:
	minikube start

dockerbuild:
	./build.sh

runctl:
	minikube kubectl -- apply -f deploy.yml
	minikube kubectl -- apply -f service.yml
	minikube kubectl -- apply -f hpa.yml
	minikube kubectl -- apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

stresstest:
	./hey -n 25000 -c 120 -m POST -q 30 http://$(MINIKUBEIP):30080/prompt/client

deletectl:
	minikube kubectl -- delete deploy llm-backend-service
	minikube kubectl -- delete service llm-backend-service
	minikube kubectl -- delete hpa backend-service-hpa

shutdown:
	docker system prune -a
	docker volume prune -a
	eval $$(minikube docker-env -u)
	minikube stop
	docker system prune -a
	docker volume prune -a