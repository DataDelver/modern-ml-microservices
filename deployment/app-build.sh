#! /usr/bin/env bash

# This script builds a Docker image for the app.
# Usage: ./app-build.sh

cd $(dirname "$0")/.. || exit 1

# Run tests
pytest --cov

# Build the Docker image for the app
docker build -t modern-ml-microservices-app .