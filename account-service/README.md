## Docker setup

### Build
docker build -t account-service:latest  .

## Run
docker run  -it account-service:latest  
docker run -p 5000:5000 -e JAEGER_HOST=localhost -e USER_API=user.localhost:5001 account-service:latest

### Services
http://localhost:5000/create-account


## k8s

+Test the service using curl
kubectl run mycurlpod --image=curlimages/curl -i --rm --tty -- sh 
curl http://account-service.account-service.svc.cluster.local:5000/create-account
