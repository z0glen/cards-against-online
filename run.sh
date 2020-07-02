#!/bin/bash
docker build -t web:latest .
docker run -e "PORT=8765" -p 8080:8765 web:latest