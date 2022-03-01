#!/usr/bin/env sh

# docker login -u kukkalli -p c3360058-8abf-4091-b178-d3d94bc18636

docker build -t orchestrator -f orchestrator/docker/Dockerfile .

#docker image tag orchestrator kukkalli/orchestrator:latest
#docker image tag orchestrator kukkalli/orchestrator:0.0.1

# docker image push kukkalli/orchestrator:latest
# docker image push kukkalli/orchestrator:0.0.1
