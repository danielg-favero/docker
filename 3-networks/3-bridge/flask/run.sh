#!/bin/bash
docker run -d -p 8000:8000 --name flask-container --rm --network flask-network flask