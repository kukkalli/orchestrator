#!/bin/bash

OLD_VERSION=0.4.4
VERSION=0.4.5

docker-compose -f docker-compose/docker-compose.yaml down

docker rmi orchestrator
docker rmi kukkalli/orchestrator
docker rmi kukkalli/orchestrator:$OLD_VERSION
docker rmi kukkalli/orchestrator:$VERSION

docker build -t orchestrator --no-cache -f docker/Dockerfile .

docker image tag orchestrator kukkalli/orchestrator:latest
docker image tag orchestrator kukkalli/orchestrator:$VERSION

REGEX='^([0-9]+\.){0,2}(\*|[0]+)$'

# shellcheck disable=SC2039
if [[ $VERSION =~ $REGEX ]]; then
  echo "INFO:<--> Uploading image to Docker Hub with Version: $VERSION"
  docker login -u kukkalli -p c3360058-8abf-4091-b178-d3d94bc18636
  docker image push kukkalli/orchestrator:latest
  docker image push kukkalli/orchestrator:$VERSION
  echo "INFO:<--> Uploaded image to Docker Hub with Version: $VERSION"
fi

# docker-compose -f docker-compose/docker-compose.yaml up -d orchestrator

exit 0
