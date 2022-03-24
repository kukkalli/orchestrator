#! /usr/bin/env sh

cp ./create-docker.sh orchestrator/docker/create-docker.sh

old_version=0.1.0
version=0.1.1

#docker login -u kukkalli -p c3360058-8abf-4091-b178-d3d94bc18636
docker rmi orchestrator
docker rmi kukkalli/orchestrator
docker rmi kukkalli/orchestrator:$old_version
docker rmi kukkalli/orchestrator:$version

docker build -t orchestrator --no-cache -f orchestrator/docker/Dockerfile .

docker image tag orchestrator kukkalli/orchestrator:latest
docker image tag orchestrator kukkalli/orchestrator:$version

docker image push kukkalli/orchestrator:latest
docker image push kukkalli/orchestrator:$version
