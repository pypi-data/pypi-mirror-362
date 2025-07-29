#!/bin/sh
# Build the Docker image for the TechLens agent
# Usage: ./build-docker.sh
docker build . -t techlens-agent:dev
