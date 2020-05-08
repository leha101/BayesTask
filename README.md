# Bayes challenge task for Python Backend Developer position

## Challenge task description

### Intro

JSON formatted messages are being published into a RabbitMQ queue (can be done manually on the RabbitMQ management UI).
Each one of the messages represents detailed information for an eSports event and has a source referenced. Your task is to read them, save them (update if necessary) and provide the information for further use.

Do not change the content of the message JSONs, since their content is intended to be as they are and they must be consumed in order.

### Features
* Run RabbitMQ in a docker container (with a docker-compose configuration)
* Publish and consume messages with the Python package `pika`
* Consumed messages are stored in a database in models like:
  * Title
  * Tournament
  * Team
  * Match
  * Scores of a Team in a Match
* Expose the data either on a API or `Website`
  * List all matches with teams (and scores) and filter by `title`, `tournament`, `state`, `date_start__gte`and `date_start_lte`
  * Detail view of a match

### Bonus
* Handle RabbitMQ exceptions (disconnect, service unreachable, etc.)
* Add logging through Python's `logging`
* Serve API data through ElasticSearch (service description in docker-compose.yml)
* Try to merge similar items together - propose a way to connect them together

Aim for completing the flow of information from receiving it to exposing it. We value your time, so choose to do some of the bonus features if you have time and take the ones you are most experienced and familiar with.

Give yourself four to six hours to complete the challenge. As a result we expect a docker-compose configuration to run the backend, consumer and RabbitMQ and your code as link to a repo on github or bitbucket with a README. Describe your choices and decisions in a few words.

Preferred usage of Python packages:
- django
- django-restframework
- flask
- flask-restful
- pika
- elasticsearch-dsl
- django-elasticsearch-dsl
- django-elasticsearch-dsl-drf

## Challenge task implementation

### Infrastructure

Task solution is implemented with docker containers managed by docker-compose. There are three docker containers in the task each serving each own service.

* rabbitmq-manager container - initiated from standard pre-build image. This container hosts the rabbitmq service responsible for handling messages send/received by the pika python module.
* mariadb container          - initiated from standard pre-build image. This container hosts and serves django project database. Container is build with volumes mapping which insures that database data will stay persistent even after the container would be turned off.

* django container           - custom build image for challenge task solution. This container hosts: 
	* python 3.8.2
	* django service ( ver 3.0.2 )
	* apache web server serving as a frontend for django
		
	This container exposes two ports for external access
		* 8082 - for apache service access
		* 8000 - for django server direct access (used for debugging) 
		
	*django project structure consist of :
		- challengetask project
		- dataholder application responsible for REST api functionality
		- api folder holds REST API configuration
		- pikaconsumer application responsible for pika messenger functionality
		- tools directory holding pika send messages demo script with several demo message files
		
		*django project models schema consist of three tables. Score, Team, Match
			NOTE : It is possible to separate data into more tables however since the task was not clear the exact separation current configuration should be sufficient to show the possibilities of working with different related tables.
	
		build
		│	 ── django
		│   ├── Dockerfile
		│   ├── scripts
		│   └── src
		│       ├── challengetask
		│       ├── dataholder
		│       │   ├── api
		│       ├── pikaconsumer
		│       └── static
		├── docker-compose.yml
		├── mariadb
		├── rabbitmq
		└── tools
			├── msg1.json
			├── msg2.json
			├── msg3.json
			├── msg4.json
			└── sendTestMsg.py

		
### Assumptions
	
	While working on the task a few assumptions had been made. 
	
		* Django is left in debug mode - since this is a non productional exercise
		* REST API is not protected by any kind of authorization
		* Mariadb database authorisation level is minimal - the admin user is given full access to db for the sake of simplicity
		* Rabbitmq configuration is vanila as it comes from the box
		* Pika messenger configuration is vanila - only used for the purpose of testing messages senf/receive functionality.
		* Apache web server is used as a front end for django. (NOTE : It could be better to use gunicorn)
		* JSON message format validation. Since demo messages files had been provided in non valid JSON format but since the offending errors were of the same type in all files a message format fixing was done assuming these would be the only error type in messages.
		* Pika messenger listener is started as a daemon from container startup script. ( NOTE : It could be nice to switch Pika messenger management through django application mechanism)

### Setup and usage
	* To start task containers run:
				
		docker-compose up command
		
		NOTE : First mariadb service startup can take some time. The django container start is dependent on mariadb and will be suspended until database service is ready. Please wait patiently.

		Tests can be run after logging into build_django_1 container
		
			docker exec -ti build_django_1 /bin/bash
			cd src
			./manage test
			
		Create send/receive message can be tested by running

			cd build/tools
			./sendTestMsg.py -f <msg_file>

### Testing
	* Due to time restrictions only django REST API basic tests had been created and used as demo to more robust posible tests
		* REST API list view test
		* REST API detail view test
		
		TODO : tests for message send/receive and database upload ideally should be added

### Known issues and suggestions 
	* Elasticsearch functionality had been left out of the scope.
	* pika start up should be handled by django server by registering into 


