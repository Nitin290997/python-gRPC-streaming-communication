#!/bin/bash

# Define variables
LOG_DIR="./logs"
SERVER_LOG_FILE="$LOG_DIR/server.log"
CLIENT1="$LOG_DIR/client1.log"
CLIENT2="$LOG_DIR/client2.log"

# Empty log files
> "$SERVER_LOG_FILE"
> "$CLIENT1"
> "$CLIENT2"

# Define the name of the network
NETWORK_NAME="my_vehicle_network"

# Check if the network exists
if docker network inspect "$NETWORK_NAME" &> /dev/null; then
    # If the network exists, delete it
    docker network rm "$NETWORK_NAME"
    echo "Network '$NETWORK_NAME' deleted."
else
    echo "Network '$NETWORK_NAME' does not exist."
fi

echo "Create Vehicle network Domain"
docker network create "$NETWORK_NAME"



# Define variables
SERVER_IMAGE_NAME="network_server"
SERVER_CONTAINER_NAME="network_server"
SERVER_DOCKERFILE_PATH="./Dockerfile-Server"
DOCKER_BUILD_CONTEXT="./"

# Build the Docker image
docker build -t "$SERVER_IMAGE_NAME" -f "$SERVER_DOCKERFILE_PATH" "$DOCKER_BUILD_CONTEXT"

# Check if a container with the same name is running
if docker ps -a --format '{{.Names}}' | grep -q "^$SERVER_CONTAINER_NAME$"; then
    # If a container with the same name is running, stop and remove it
    docker stop "$SERVER_CONTAINER_NAME" && docker rm "$SERVER_CONTAINER_NAME"
    echo "Existing container '$SERVER_CONTAINER_NAME' stopped and removed."
fi

# Run a new container in the background if no container with the same name is running
if ! docker ps -a --format '{{.Names}}' | grep -q "^$SERVER_CONTAINER_NAME$"; then
    docker run -itd --network "$NETWORK_NAME" --name "$SERVER_CONTAINER_NAME" -p 8010:8010 -v ./logs/:/root/logs "$SERVER_IMAGE_NAME"
    echo "New container '$SERVER_CONTAINER_NAME' started."
fi


# Define function to build and run container
build_and_run_container() {
    local IMAGE_NAME="$1"
    local CONTAINER_NAME="$2"
    local DOCKERFILE_PATH="$3"

    # Build the Docker image
    docker build -t "$IMAGE_NAME" -f "$DOCKERFILE_PATH" "$DOCKER_BUILD_CONTEXT"

    # Check if a container with the same name is running
    if docker ps -a --format '{{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
        # If a container with the same name is running, stop and remove it
        docker stop "$CONTAINER_NAME" && docker rm "$CONTAINER_NAME"
        echo "Existing container '$CONTAINER_NAME' stopped and removed."
    fi

    # Run a new container in the background if no container with the same name is running
    if ! docker ps -a --format '{{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
        docker run -itd --network "$NETWORK_NAME" --name "$CONTAINER_NAME" -v ./logs/:/root/logs "$IMAGE_NAME"
        echo "New container '$CONTAINER_NAME' started."
    fi
}

# Define variables for DEM container
CLIENT1_IMAGE_NAME="client1"
CLIENT1_CONTAINER_NAME="client1_container"
CLIENT1_DOCKERFILE_PATH="./Dockerfile-client1"

# Call the function to build and run DEM container
build_and_run_container "$CLIENT1_IMAGE_NAME" "$CLIENT1_CONTAINER_NAME" "$CLIENT1_DOCKERFILE_PATH"

# Define variables for DCM container
CLIENT2_IMAGE_NAME="client2"
CLIENT2_CONTAINER_NAME="client2_container"
CLIENT2_DOCKERFILE_PATH="./Dockerfile-client2"

# Call the function to build and run DCM container
build_and_run_container "$CLIENT2_IMAGE_NAME" "$CLIENT2_CONTAINER_NAME" "$CLIENT2_DOCKERFILE_PATH"