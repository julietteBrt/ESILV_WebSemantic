# Web semantic project

# Installation

Clone this repository and `cd` into it:
```
$ git clone https://github.com/charlyalizadeh/ESILV_WebSemantic
$ cd ESILV_WebSemantic
```

## Fuseki

### Create the triplestore

The following instructions explain how to install fuseki with docker. [(Install without docker)](https://jena.apache.org/documentation/fuseki2/#download-fuseki)
1. Pull the docker image:
```bash
$ docker pull stain/jena-fuseki
```
2. Create a docker volume for data persistence:
```bash
$ docker run --name fuseki-data -v /fuseki busybox
```
3. Create the fuseki container (you can change the admin password if you like):
```bash
$ docker run -d --name fuseki -p 3030:3030 --volumes-from fuseki-data -e ADMIN_PASSWORD=pw stain/jena-fuseki
```
4. Enter the container and install `procps` (required to stop and restart the container without errors)
```bash
$ docker exec -it fuseki bash
/jena-fuseki$ apt-get upgrade
/jena-fuseki$ apt-get install -y --no-install-recommends procps
```
Now go on [http://localhost:3030](http://localhost:3030) and you should be able to access the fuseki web interface (user: *admin*, password: *pw*)

### Import the data

1. Unzip `gtfsintriples.zip`
```bash
$ unzip gtfsintriples.zip
```
2. Create the `gtfs` database
![add dataset](doc/adddataset.png)
3. Upload `gtfsintriples.ttl` to the database (it can take a while):
![upload dataset](doc/uploaddata.png)

The fuseki triplestore is now configured to work with the flask application


## Flask

1. Create a [virtual environment](https://docs.python.org/3/tutorial/venv.html) and activate it:
```bash
$ python3 -m venv .venv
$ source .venv/bin/activate # On windows: .venv\Scripts\activate.bat
```
2. Install the requirements
```bash
$ pip install -r requirements.txt
```
3. Setup the environment variables
```
# Linux and MacOS:
$ export FLASK_APP=flaskr
$ export FLASK_ENV=development

# Windows cmd
> set FLASK_APP=flaskr
> set FLASK_ENV=development

# Windows PowerShell
> $env:FLASK_APP = "flaskr"
> $env:FLASK_ENV = "development"
```
4. Run the flask app:
```
$ flask run
```

You should be able to access our app on [http://localhost:5000/](http://localhost:5000/)

# Credits

This project relies highly on [linked-gtfs](https://github.com/OpenTransport/linked-gtfs) and [gtfs-csv2rdf](https://github.com/OpenTransport/gtfs-csv2rdf) by [Pieter Colpaert](https://github.com/pietercolpaert).
