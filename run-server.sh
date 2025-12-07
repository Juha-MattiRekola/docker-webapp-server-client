#!/bin/sh

# Luo voluumin ja verkon automaattisesti, jos niitä ei ole
docker volume inspect servervol >/dev/null 2>&1 || docker volume create servervol
docker network inspect webapp-network >/dev/null 2>&1 || docker network create webapp-network

# Rakenna ja aja palvelin. nimetään palvelimeksi, mountataan voluumi ja liitetään verkkoon. Asetetaan PORT-ympäristömuuttuja.
# Kontti käynnistetään webapp-server -kuvasta, joka on rakennettu Dockerfile.server -tiedostosta
docker build -t webapp-server -f Dockerfile.server .
docker run -d \
  --name server-container \
  --mount source=servervol,target=/serverdata \
  --network webapp-network \
  -e PORT=6000 \
  webapp-server
