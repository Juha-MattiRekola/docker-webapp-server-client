#!/bin/sh

# Luo voluumi ja verkko automaattisesti, jos niitä ei ole
docker volume inspect clientvol >/dev/null 2>&1 || docker volume create clientvol
docker network inspect webapp-network >/dev/null 2>&1 || docker network create webapp-network

# Rakennetaan kuva webapp-client Dockerfilen pohjalta. Ajetaan kontti nimellä client-container, mountataan voluumi ja liitetään verkkoon.
# Asetetaan SERVER- ja PORT-ympäristömuuttujat.
docker build -t webapp-client -f Dockerfile.client .
docker run --rm \
  --name client-container \
  --mount source=clientvol,target=/clientdata \
  --network webapp-network \
  -e SERVER=server-container -e PORT=6000 \
  webapp-client