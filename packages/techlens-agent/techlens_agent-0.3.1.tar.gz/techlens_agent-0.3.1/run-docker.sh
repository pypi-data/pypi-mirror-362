#!/bin/sh
# Run TechLens agent in a Docker container
# Mounts current directory's results folder and necessary config folders for AWS, GCP, and Azure
# Usage: ./docker-run.sh [additional arguments for TechLens agent]
docker run -it --rm \
    -v $PWD/results:/techlens/results \
    -v $HOME/.ssh:/techlens/.ssh:ro \
    -v $HOME/.aws:/techlens/.aws:ro \
    -v $HOME/.azure:/techlens/.azure:ro \
    -v $HOME/.config/gcloud:/techlens/.config/cloud:ro \
    techlens-agent:dev "$@"
