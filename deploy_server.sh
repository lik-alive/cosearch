#!/bin/bash
if [ "$1" == "--prod" ]; then
  echo "Start prod server"
  docker-compose up -d --remove-orphans --build
else 
  echo "Start dev server"
  docker-compose up --build
fi