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

runctl:
	minikube kubectl -- apply -f deploy.yml
	minikube kubectl -- apply -f service.yml
	minikube kubectl -- apply -f hpa.yml
	minikube kubectl -- apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

stresstest:
	./hey -n 25000 -c 120 -m POST -q 30 http://$(MINIKUBEIP):30080/health

deletectl:
	minikube kubectl -- delete deploy llm-backend-service
	minikube kubectl -- delete service llm-backend-service
	minikube kubectl -- delete hpa backend-service-hpa

shutdown: deletectl
	cd ./llm && make deletectl
	cd -
	eval $$(minikube docker-env -u)
	minikube stop
