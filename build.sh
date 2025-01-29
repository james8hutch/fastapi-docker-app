#!/bin/bash

# Stop and remove the existing container if it exists
docker-compose down

# Prune unused Docker resources (force without prompt)
docker system prune -f

# Build and start the containers
docker-compose up --build -d

# Check if the app container is running and healthy
echo "Waiting for the app container to be healthy..."
MAX_RETRIES=20
RETRY_INTERVAL=5
APP_CONTAINER_NAME="fastapi-app"

for ((i=1; i<=MAX_RETRIES; i++)); do
  STATUS=$(docker inspect --format='{{.State.Health.Status}}' $APP_CONTAINER_NAME 2>/dev/null)

  if [ "$STATUS" == "healthy" ]; then
    echo "✅ The app container is up and healthy!"
    exit 0
  elif [ "$STATUS" == "unhealthy" ]; then
    echo "❌ The app container is unhealthy. Check the logs:"
    docker logs $APP_CONTAINER_NAME
    exit 1
  else
    echo "⏳ Waiting for the app container to be healthy... (Retry $i/$MAX_RETRIES)"
    sleep $RETRY_INTERVAL
  fi
done

echo "❌ The app container did not become healthy after $((MAX_RETRIES * RETRY_INTERVAL)) seconds."
echo "Check the logs for details:"
docker logs $APP_CONTAINER_NAME
exit 1