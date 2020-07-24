# api_yatube
***Yatube API*** is a REST API for [Yatube](https://github.com/evgfitil/yatube) blog platform

All available endpoints and API specifications are here https://yatube.ea4ws.tk/redoc/

You can try most of the functionality use endpoints on this demo site https://yamdb.ea4ws.tk/api/v1/ or test it locally

### Developing and testing locally (Quick Start)

#### With Docker
  
  1. Clone this repository
  2. Rename `.env-docker-example` file to `.env.dev`. Customize it for your needs
  3. If you want to load the test data you can uncomment the line in `entrypoint.sh` file with:
  ```
  # python manage.py loaddata api/fixtures/db_fixtures.json
  ``` 
  
  4. Use provided `Dockerfile` and `docker-compose.yml`, build the image and run the container
  ```
  docker-compose up -d --build
  ```
  5. If You're not using the test data, you need to create Django admin user
  
  ```
  docker exec -ti <container_id> python manage.py createsuperuser
  ```
  If everything went well, you now have a server running on http://localhost:8000
  
  Run `docker image prune --filter label=stage=builder` to remove a builder image

  You can also run tests to make sure everything is ok, for that run:
  ```
  docker exec -ti <container_id> pytest
  ```
  
  You can find API specification and all available endpoints on documentation page http://localhost:8000/redoc/
  
