# Docker Images and Tags to Use
 * [mongo:4.1](https://hub.docker.com/_/mongo?tab=description)
 * [jupyter/pyspark-notebook:7254cdcfa22b](https://hub.docker.com/r/jupyter/pyspark-notebook)
 * [esridocker/arcgis-api-python-notebook](https://hub.docker.com/r/esridocker/arcgis-api-python-notebook)

# Dependencies
| Dependency | Use |
|---|---|
| [ics](https://icspy.readthedocs.io/en/v0.4/) | This will help to parse *.ics calendar data gathered from realty websites. |
| [Flask](http://flask.pocoo.org/) | Used to create REST services. |
| [virtualenv](hhttps://virtualenv.pypa.io/en/latest/) | Needed by Flask. |

To run the `docker-compose.yml` you will need another environment variables file called `credentials.yml` with the your Esri Developer username and password like the snippet below.
```
ESRI_USERNAME=foo
ESRI_PASSWORD=bar
```

# Running the suite
To get the suite of docker containers running just run `fresh_start.sh`. Once the scripts complete try visiting the following pages to test out the Flask service.
 * http://127.0.0.1:5000
 * http://127.0.0.1:5000/get_geocode/\<ADDRESS>
 * http://127.0.0.1:5000/get_directions/\{"source":\<ADDRESS>, "destination":\<ADDRESS>\}