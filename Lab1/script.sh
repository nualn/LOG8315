#!/bin/bash


setup() {
    echo "Executing environment setup..."
    docker build -t container .
    docker run -v $(pwd)/app/data:/app/data container run_setup.py
}

benchmark() {
    echo "Running benchmark..."
    docker run -v $(pwd)/app/data:/app/data container run_benchmark.py
}

case "$1" in
    "setup")
        setup
        ;;
    "benchmark")
        benchmark
        ;;
esac


