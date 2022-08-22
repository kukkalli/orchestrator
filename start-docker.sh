#!/bin/bash

docker-compose -f docker-compose/docker-compose.yaml down

sleep 10

docker-compose -f docker-compose/docker-compose.yaml up -d orchestrator

exit 0
