#!/bin/bash

./docker-compose-down.sh
./docker-compose-up.sh

./install-deps.sh

docker logs esri
docker logs pyspark

docker exec esri python /home/jovyan/work/get_directions.py &