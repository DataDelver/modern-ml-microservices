#! /usr/bin/env bash

# This script starts the MLflow server on localhost:9999
# Ensure the script is run from the directory where it is located
# Usage: ./start-mlflow.sh

# Check if MLflow is installed
if ! command -v mlflow &> /dev/null
then
    echo "MLflow could not be found. Please install it first."
    exit 1
fi

cd $(dirname "$0")
mlflow server --host 127.0.0.1 --port 9999