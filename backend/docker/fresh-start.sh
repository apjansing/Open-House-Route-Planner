#!/bin/bash

./docker-compose-down.sh
./docker-compose-up.sh

./install-deps.sh

docker logs esri
docker logs pyspark

./start_flask_apps.sh