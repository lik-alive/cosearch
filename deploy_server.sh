#!/bin/bash
if [ "$1" == "--prod" ]; then
  echo "Start prod server"
  env MODE=production docker-compose up -d --remove-orphans --build
else 
  echo "Start dev server"
  env MODE=development docker-compose up --build
fi