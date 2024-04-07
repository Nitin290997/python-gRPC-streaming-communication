# python-gRPC-streaming-communication

### Description:
This repository showcases a gRPC-based server and client implementation, demonstrating a method of communication where the server responds to client requests with streaming data. In this setup, a single Remote Procedure Call (RPC) handles both the request and acknowledgment of responses, creating a continuous and efficient exchange between the client and server.

gRPC offers bidirectional streaming communication. This means both the client and the server can send and receive multiple requests and responses simultaneously on a single connection. REST does not offer this feature.

#### Key Features:

* Utilizes gRPC for efficient and scalable communication between client and server. 
* Demonstrates streaming requests and responses, allowing for real-time updates and data synchronization. 
* The server responds to client calls only when there's an update in the requested data, minimizing unnecessary communication. 
* RPCs persist indefinitely, ensuring continuous connectivity between client and server.

This project serves as a practical example of leveraging gRPC for streaming communication, offering insights into building robust and responsive client-server interactions.

# Table of Contents

# Installation Instruction

### Requisites

1. Docker
2. Python3.11

# Usage

Repo is designed to be used in windows as well as linux environment. For linux users, a bash script is also provided to easily create logs and clean and build images and run containers with mounted path and stop containers with already running.

```shell
bash setup.sh
```

#### For windows users

Clean the logs in the logs directory named as 
1. server.log
2. client1.log
3. client2.log

Create a local network for docker containers to communicate with each other. Check if the network exists delete it and create again
```shell
// To delete a existing network
docker network rm "$NETWORK_NAME"

// To create a network
docker network create "$NETWORK_NAME"
```

Once the network is created .. Build the image

```shell
docker build -t Dockerfile-Server -f network_server ./
```

Check if the container is existing if yes stop and remove it and run new

```shell
// To stop container
docker stop netwrok_server_container

// To remove
docker stop netwrok_server_container

// To run new container
docker run -itd --network "$NETWORK_NAME" --name netwrok_server_container -p 8010:8010 -v ./logs/:/root/logs network_server
```

Once server is running. build the image for the clients using the below commands using values

```shell
// For Client 1
CLIENT_IMAGE_NAME="client1"
CLIENT_CONTAINER_NAME="client1_container"
CLIENT_DOCKERFILE_PATH="./Dockerfile-client1"

// For Client 2
CLIENT_IMAGE_NAME="client2"
CLIENT_CONTAINER_NAME="client2_container"
CLIENT_DOCKERFILE_PATH="./Dockerfile-client2"

// To build client image
docker build -t "$CLIENT_IMAGE_NAME" -f "$CLIENT_DOCKERFILE_PATH" ./

// To stop and remove container
docker stop "$CLIENT_CONTAINER_NAME" && docker rm "$CLIENT_CONTAINER_NAME"

// To run new container
docker run -itd --network "$NETWORK_NAME" --name "$CLIENT_CONTAINER_NAME" -v ./logs/:/root/logs "$CLIENT_IMAGE_NAME"
```