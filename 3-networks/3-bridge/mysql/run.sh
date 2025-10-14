#!/bin/bash
docker run -d -p 3306:3306 --name flask-mysql-container --rm --network flask-network -e MYSQL_ALLOW_EMPTY_PASSWORD=true flask-mysql
