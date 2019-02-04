# Docker Images and Tags to Use
 * [mongo:4.1](https://hub.docker.com/_/mongo?tab=description)
 * [jupyter/pyspark-notebook:7254cdcfa22b](https://hub.docker.com/r/jupyter/pyspark-notebook)
 * [esridocker/arcgis-api-python-notebook](https://hub.docker.com/r/esridocker/arcgis-api-python-notebook)

# Dependencies
| Dependency | Use |
|---|---|
| [ics](https://icspy.readthedocs.io/en/v0.4/) | This will help to parse *.ics calendar data gathered from realty websites. |

To run the `docker-compose.yml` you will need another environment variables file called `credentials.yml` with the your Esri Developer username and password like the snippet below.
```
ESRI_USERNAME=foo
ESRI_PASSWORD=bar
```