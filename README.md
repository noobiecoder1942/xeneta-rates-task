# xeneta-rates-task
Solution to Xeneta's Rates Task Challenge

## Instructions to run application

* Clone this repository to your local machine.
* In the home directory, run:
```sudo docker compose up --build```
* From your browser make a request as such:
```http://localhost:3000/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=scandinavia```

### Instructions to run unit test suite

* While the containers are running (following above steps), run the following: ```sudo docker compose exec flask-app pytest```

## My Development Environment
* Ubuntu 22.04.4 LTS
* Docker 27.0.3
* Python 3.10.12

## Approximate Time Spent
* Core (Flask App and SQL query): 4 hours
* Extras (PEP8 style checks, Unit tests, Docker and Docker Compose): 4 hours

## Data definition

A database dump is provided that includes the following information:

### Ports

Information about ports, including:

* 5-character port code
* Port name
* Slug describing which region the port belongs to

### Regions

A hierarchy of regions, including:

* Slug - a machine-readable form of the region name
* The name of the region
* Slug describing which parent region the region belongs to

Note that a region can have both ports and regions as children, and the region
tree does not have a fixed depth.

### Prices

Individual daily prices between ports, in USD.

* 5-character origin port code
* 5-character destination port code
* The day for which the price is valid
* The price in USD