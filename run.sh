#!/bin/bash
docker build -t z0glen/cards-against-online .
docker run -e "PORT=8765" -p 8080:8765 z0glen/cards-against-online