#! /usr/bin/env bash

# This script builds a Docker image for an MLflow model using the specified model URI.
# It uses the MLflow CLI to create the Docker image and enables MLServer for serving the model.
# Usage: ./model-docker-build.sh <model_uri> <image_tag>

# Ensure that MLflow is installed and available in your environment.
# Make sure to replace the model URI with your actual model URI if needed.
# Example model URI: runs:/<run_id>/model

# Check if MLflow is installed
if ! command -v mlflow &> /dev/null
then
    echo "MLflow could not be found. Please install it first."
    exit 1
fi

# Generate the Docker File for the Model
cd $(dirname "$0")/.. || exit 1
mlflow models generate-dockerfile --model-uri $1 --output-directory build --enable-mlserver

# Build the Docker image for the MLflow model
docker build -t $2 build