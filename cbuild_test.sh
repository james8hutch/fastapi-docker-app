#!/bin/bash

# Stop and remove existing test container (if any)
docker-compose down

# Prune unused Docker resources (force without prompt)
docker system prune -f

# Force rebuild the services to pick up code changes
echo "Rebuilding images..."
docker-compose build --no-cache

# Start the database and wait for it to be ready
echo "Starting the database container..."
docker-compose up --build -d db

# Wait for the database to become healthy
echo "Waiting for the database container to be healthy..."
MAX_RETRIES=20
RETRY_INTERVAL=5
DB_CONTAINER_NAME="fastapi-db"

for ((i=1; i<=MAX_RETRIES; i++)); do
  STATUS=$(docker inspect --format='{{.State.Health.Status}}' $DB_CONTAINER_NAME 2>/dev/null)

  if [ "$STATUS" == "healthy" ]; then
    echo "✅ The database container is up and healthy!"
    break
  elif [ "$STATUS" == "unhealthy" ]; then
    echo "❌ The database container is unhealthy. Check the logs:"
    docker logs $DB_CONTAINER_NAME
    exit 1
  else
    echo "⏳ Waiting for the database container to be healthy... (Retry $i/$MAX_RETRIES)"
    sleep $RETRY_INTERVAL
  fi
done

if [ "$STATUS" != "healthy" ]; then
  echo "❌ The database container did not become healthy after $((MAX_RETRIES * RETRY_INTERVAL)) seconds."
  echo "Check the logs for details:"
  docker logs $DB_CONTAINER_NAME
  exit 1
fi

# Run the migration container to apply migrations
echo "Applying database migrations..."
#docker-compose run --rm migrate

# Run the test container and stream logs
echo "Running tests..."
#docker-compose up --build --abort-on-container-exit --exit-code-from test
docker-compose run --rm test

# Capture the exit code of the test container
TEST_EXIT_CODE=$?
echo "TEST_EXIT_CODE: $TEST_EXIT_CODE"

# Tear down the containers after tests
echo "Tearing down containers..."
docker-compose down

# Check the exit code of the test container and handle success/failure
if [ $TEST_EXIT_CODE -eq 0 ]; then
  echo "✅ Tests completed successfully."
  exit 0
else
  echo "❌ Tests failed. Check the logs below for more details."
  # Show the logs from the test container if tests failed
  docker-compose logs test
  exit 1
fi
