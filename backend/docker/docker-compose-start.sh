#!/bin/bash

docker-compose up -d
docker exec esri pip install -r requirements.txt