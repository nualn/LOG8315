#!/bin/bash


setup() {
    echo "Executing environment setup..."
    docker build -t tp1-container .
    docker run -v $(pwd)/app/data:/app/data tp1-container run_setup.py
}

benchmark() {
    echo "Running benchmark..."
    docker run -v $(pwd)/app/data:/app/data tp1-container run_benchmark.py
}

case "$1" in
    "setup")
        setup
        ;;
    "benchmark")
        benchmark
        ;;
    *)
        setup
        benchmark
esac
