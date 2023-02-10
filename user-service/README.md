## Docker setup

### Build
docker build -t user-service:latest . 

## Run
docker run  -it user-service:latest  bash
docker run --entrypoint /bin/bash  -it user-service:latest
docker run -p 5001:5001 user-service:latest

### Services
http://localhost:5001/save-user

## k8s
minikube image load user-service:0.1.0
(este si funciono, se me hace que no hice bien el image)
kubectl run user-service --image=user-service:latest --image-pull-policy=Never

kubectl apply -f .k8s/deployment.yaml

+Test the service using curl
kubectl run mycurlpod --image=curlimages/curl -i --rm --tty -- sh 
http://user-service.user-service.svc.cluster.local:5001/save-user

+Check the traces in jaeger UI
kubectl port-forward svc/simplest-query -n observability 16686:16686
++Jager UI
http://localhost:16686/search 


## Create k8s resources
kubectl apply -k .k8s/