# Buylando API
![GitHub repo size](https://img.shields.io/github/repo-size/FMularski/ecommerce-api?color=red)
![GitHub last commit](https://img.shields.io/github/last-commit/FMularski/ecommerce-api?color=blue)
![GitHub top language](https://img.shields.io/github/languages/top/FMularski/ecommerce-api?color=green)

## 🛒 Created with
* Django 4.2
* Django Rest Framework 3.14.0
* drf-yasg 1.21.5
* Postgres
* Nginx
* Celery 5.2.7
* RabbitMQ
* Docker

## 🛒 About
Buylando is an API project allowing to browse and manage products and orders from an online store. The project itself consists of five docker containers being: 
* the web application
* a relational database
* a reverse proxy server for serving the static content
* a celery worker for sending emails to users
* a rabbitmq server as a message broker

The project was created as a recruitment task.

## 🛒 Core features
* User authentication (JWT)
* Getting the list of all products
* Getting the list of the most popular products
* Getting a particular product by its id
* Creating new products (sellers only)
* Updating existing products (sellers only)
* Deleting products
* Creating orders (customers only)
* Browsing objects with the admin panel
* Sending email (console.EmailBackend) with order confirmations and payment reminders
* Auto creating 200x200 miniatures of uploaded images (products images) 

## 🛒 Launching and usage

* Download the project to your local machine
```bash
git clone https://github.com/FMularski/ecommerce-api.git
```
* Create buylando/.env file with the following content:
```bash
SECRET_KEY='top-secret'

POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```
* Start the project with docker
```bash
docker compose up
```
During the booting up the database is migrated and sample data is populated, such as users, products and orders. Please wait until all containers are ready.
* Open the app in your browser at
```bash
http://localhost:80
```
* Have fun with the project by interacting with the provided open API or use any other client of your choice. You can also go to the admin panel to inspect existing objects.
```bash
http://localhost/admin
```
SU credentials:
email: admin@mail.com
password: admin
