## Run jaegertracing
docker run --rm -d --name jaeger \
  -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 \
  -e COLLECTOR_OTLP_ENABLED=true \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 4317:4317 \
  -p 4318:4318 \
  -p 14250:14250 \
  -p 14268:14268 \
  -p 14269:14269 \
  -p 9411:9411 \
  jaegertracing/all-in-one:1.38

+ Jaeger UI
http://localhost:16686/

---

## Local setup
pipenv install -r requirements.txt
pipenv shell

---

## Run locally
*Run jaeger usign docker image
1. Run user service
JAEGER_HOST=localhost python3 user-service/user.py
2. Run account service (require user service)
JAEGER_HOST=localhost USER_API=localhost:5001 python3 account-service/account.py

### Services
http://localhost:5000/create-account
http://localhost:5001/save-user

## Docker
docker build -t user-service:latest  .
docker run  -it user-service:latest 

## Install Jaeger in k8s (minikube)
+ Reference https://faun.pub/how-to-deploy-jaeger-on-kubernetes-69cf48447182 

1. Install CertManager
```helm install example example_chart --namespace example --create-namespace --set cert-manager.namespace=security```

2. Install Jaeger operator
```kubectl create -f https://github.com/jaegertracing/jaeger-operator/releases/download/v1.36.0/jaeger-operator.yaml -n observability```

3. Test it
```
+Port forward
kubectl port-forward svc/simplest-query -n observability 16686:16686
++Jager UI
http://localhost:16686/search
```
