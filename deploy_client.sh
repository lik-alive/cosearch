#!/bin/bash
if [ "$1" == "--prod" ]; then
  echo "Start prod client"
  (cd client && yarn build)
else 
  echo "Start dev client"
  (cd client && yarn astart)
fi