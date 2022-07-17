#!/usr/bin/env bash
up() {
  echo "Starting Airbyte..."
  docker-compose -f docker-compose-airbyte.yaml down
  docker-compose -f docker-compose-airbyte.yaml up -d

  echo "Starting Airflow..."
  docker-compose -f docker-compose-airflow.yaml down
  docker-compose -f docker-compose-airflow.yaml up -d
  echo "Access Airflow at http://localhost:8080 to kick off your Airbyte sync DAG."
}

down() {
  echo "Stopping Airbyte..."
  docker-compose -f docker-compose-airbyte.yaml down
  echo "Stopping Airflow..."
  docker-compose -f docker-compose-airflow.yaml down
}

case $1 in
  up)
    up
    ;;
  down)
    down
    ;;
  *)
    echo "Usage: $0 {up|down}"
    ;;
esac
