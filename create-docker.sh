#! /usr/bin/env sh

old_version=0.1.2
version=0.1.3

docker rmi orchestrator
docker rmi kukkalli/orchestrator
docker rmi kukkalli/orchestrator:$old_version
docker rmi kukkalli/orchestrator:$version

docker build -t orchestrator --no-cache -f docker/Dockerfile .

docker image tag orchestrator kukkalli/orchestrator:latest
docker image tag orchestrator kukkalli/orchestrator:$version

# docker login -u kukkalli -p c3360058-8abf-4091-b178-d3d94bc18636
# docker image push kukkalli/orchestrator:latest
# docker image push kukkalli/orchestrator:$version
