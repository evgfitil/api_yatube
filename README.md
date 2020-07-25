# api_yatube
***Yatube API*** is a REST API for [Yatube](https://github.com/evgfitil/yatube) blog platform

All available endpoints and API specifications are here https://yatube.ea4ws.tk/redoc/

Demo site https://yatube.ea4ws.tk/api/v1/ available with authentication methods and anonymous access

### Developing and testing locally (Quick Start)

#### With Docker
  
  1. Clone this repository
  
  2. Copy or rename `.env-docker-example` file to `.env`. Customize it for your needs
  
  4. Use provided `Dockerfile` and `docker-compose.yml`, build the image and run the container
  ```
  docker-compose up -d --build
  ```
  5.Create Django admin user
  
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
  
  #### Without Docker

If You want to test API locally:
  1. Clone this repository
  2. Copy or rename `.env-example` file to `.env`
  3. Create and activate a virtual environment
  ```
python3 -m venv venv
source ./venv/bin/activate
  ```
  4. Install dependencies
  ```
pip install -r requirements.txt
```
  6. Create a Django admin user and apply migrations
 ```
 python manage.py migrate
 python manage.py createsuperuser
 ```
  7. Start API server locally
```
python manage.py runserver
```
If everything went well, you now have a server running on http://localhost:8000

You can also run `pytest` to make sure everything is ok

API specification and all endpoints available on documentation page http://localhost:8000/redoc/
