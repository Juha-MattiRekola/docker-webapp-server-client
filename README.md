# Webapp Server and Client with Docker

This project contains a simple TCP server and client that communicate between Docker containers.  
**The server container** generates a random 1KB text, calculates its SHA‑256 checksum, and sends it to the client.  
**The client container** receives the data, stores it in a volume, and verifies that the checksum matches.

#### Workflow diagram

Server (random.txt) ---> sends data + checksum ---> Client (received.txt)


---------------------------------------------------------------------------------------------------

## Quick Start

If you already have Docker installed, you can jump right in:

- Start Docker
- Run the following commands:

```bash
git clone https://github.com/Juha-MattiRekola/docker-webapp-server-client.git

cd docker-webapp-server-client         # move to the right directory

chmod +x run-server.sh run-client.sh   # give scripts execution rights

./run-server.sh                        # build and start the server container

./run-client.sh                        # build and run the client container

docker logs server-container           # check server logs
```

#### Optional part

Client - received data from the server to the textfile "received.txt"

```bash
docker run --rm -it \
  --mount source=clientvol,target=/clientdata \
  alpine:latest \
  cat /clientdata/received.txt
```

Server - Check if the client data is similar to this random data that server created

```bash
docker run --rm -it \
  --mount source=servervol,target=/serverdata \
  alpine:latest \
  cat /serverdata/random.txt
```
  
## Prerequisites

- **1. Install [Docker](https://docs.docker.com/get-docker/) on your system.**
  - On **Windows/Mac**, use Docker Desktop.
  - On **Linux**, install Docker Engine via your package manager.
- Verify installation by running:

  ```bash
  docker --version
  ```

- **2. Clone the project from GitHub**

 ```bash
  # Get project from the GitHub
  git clone https://github.com/Juha-MattiRekola/docker-webapp-server-client.git

  # Move to the right directory
  cd docker-webapp-server-client
  ```

## Running the Application

### 1. Script execution rights

If you encounter the error (for example: "-bash: ./run-server.sh: Permission denied"),
Grant execution rights to the scripts:

```bash
chmod +x run-server.sh run-client.sh
```

### 2. Start the Server

```bash
./run-server.sh
```

- This creates the servervol volume and webapp-network automatically, if they don't already exist (*Volumes are used to persist files outside the container lifecycle, so the data remains available even after the container stops.*)
- Builds the webapp-server image from Dockerfile.server
- Runs the container named server-container in detached mode. Detached mode means that the server container runs in the background. So it does not block the terminal.

### 3. Start the Client

```bash
./run-client.sh
```

- Creates the clientvol volume and webapp-network network automatically if they don't exist (*Volumes are used to persist files outside the container lifecycle, so the data remains available even after the container stops.*)
- Builds the webapp-client image from Dockerfile.client
- Runs the container named client-container
- The client runs once and then exits. Note that the client container is removed automatically after execution.

## Verifying the functionality

### Testing and inspecting logs

#### Server logs

- Since the server runs in detached mode, its print messages appear in Docker logs.
- Inspect logs with command:

```bash
docker logs server-container
```

- Response example (The port number will most likely be different from the example):

```bash
Palvelin kuuntelee portissa 6000
Yhdistetty osoitteesta ('172.23.0.3', 55144)
```
Log output (translated from Finnish):

"Server listening on port 6000
Connected from ('172.23.0.3', 55144)"


#### Client logs

- The client prints a success message:

```bash
Tiedoston siirto onnistui, SHA-256 tarkistussumma täsmää
```
Success message (translated from Finnish):
"File transfer successful, SHA-256 checksum matches. Congratulations!"


### File verification

Both files are stored in Docker volumes (clientvol and servervol), which allow data to persist independently of container execution.

#### Client's received file

- The file is stored in the clientvol volume at /clientdata/received.txt
- To check its contents you can run:

```bash
docker run --rm -it \
  --mount source=clientvol,target=/clientdata \
  alpine:latest \
  cat /clientdata/received.txt
```

#### Server's generated file

- The server stores the random text in the servervol volume at /serverdata/random.txt.

- To check its contents you can run:

```bash
docker run --rm -it \
  --mount source=servervol,target=/serverdata \
  alpine:latest \
  cat /serverdata/random.txt
```

#### Comparison

- The contents of /clientdata/received.txt and /serverdata/random.txt should be identical.
- Additionally, the SHA-256 checksum must match, confirming the transfer was successful.

### Common issues

**Container name already in use**

If you see for example:

```bash
docker: Error response from daemon: Conflict. The container name "/server-container" is already in use...
```
You can remove the old container with ("server-container" is the name of the server container that starts after successfully starting the server):

```bash
docker rm -f server-container
```

**Alpine image not found**

On the first run, Docker will automatically pull the Alpine image:

```bash
Unable to find image 'alpine:latest' locally
latest: Pulling from library/alpine
Status: Downloaded newer image for alpine:latest
```

## Cleanup instructions

When you are finished testing, you may want to remove all containers, volumes, networks, and images created by this project to free disk space and avoid conflicts.

### 1. Stop and remove containers

```bash
docker rm -f server-container client-container
```

- -f forces removal even if the container is still running
- Client container should already be removed. Therefore it gives you an error: Error response from daemon: No such container: client-container

### 2. Remove volumes

```bash
docker volume rm servervol clientvol
```

- This deletes the stored files (random.txt and received.txt) from Docker volumes.

### 3. Remove network

```bash
docker network rm webapp-network
```

- Removes the custom network used for communication between server and client.

### 4. Remove images

```bash
docker rmi webapp-server webapp-client
```

- Deletes the images built from Dockerfile.server and Dockerfile.client.

### 5. Delete docker-webapp-server-client and its contents

```bash
cd ..                                # Move to the previous directory
rm -rf docker-webapp-server-client   # Remove directory and its contents
```

- This removes the folder docker-webapp-server-client and everything inside it.
- **Be careful!!** Before you delete the folder, you need to make sure you are in its parent directory (the one just before docker-webapp-server-client).

### 6. Optional: prune unused resources (you might lose more than you want to)

```bash
docker system prune -a
```

- Cleans up all unused containers, networks, images, and build cache.
- **Be careful**: this removes all unused Docker resources, not just those from this project.

### Summary

Run these commands in order to completely remove everything created by the project:

```bash
docker rm -f server-container client-container
docker volume rm servervol clientvol
docker network rm webapp-network
docker rmi webapp-server webapp-client

# Remove directory and contents
cd ..
rm -rf docker-webapp-server-client
```

After running these commands, all containers, volumes, networks, and images created by **this project** will be removed.  

## Docker Hub Images
- [webapp-server](https://hub.docker.com/r/<your-username>/webapp-server)
- [webapp-client](https://hub.docker.com/r/<your-username>/webapp-client)







