#!/bin/bash
docker volume ls -f "dangling=true" --quiet | while IFS= read -r volume
do
    docker volume rm "$volume"
done