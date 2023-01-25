## Docker setup

### Build
docker build -t account-service:latest  .

## Run
docker run  -it account-service:latest  
docker run -p 5000:5000 -e JAEGER_HOST=localhost -e USER_API=user.localhost:5001 account-service:latest

### Services
http://localhost:5000/create-account
