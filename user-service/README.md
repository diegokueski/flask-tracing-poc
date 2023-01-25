## Docker setup

### Build
docker build -t user-service:latest  .

## Run
docker run  -it user-service:latest  
docker run -p 5001:5001 user-service:latest

### Services
http://localhost:5001/save-user
