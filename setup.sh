#!/usr/bin/env bash
install(){
  echo "Manage Docker as a non-root user"
  sudo groupadd docker
  sudo usermod -aG docker $USER
  newgrp docker

  echo "install snowflake connector"
  docker pull airbyte/destination-snowflake:0.4.31

  echo "install mongo connector"
  docker pull airbyte/source-mongodb-v2:0.1.15

  echo "Creating mongo database"
  echo "db.createCollection('schoolRawData')" |   mongo --username admin --password admin --authenticationDatabase admin
  echo "db.adminCommand({renameCollection: 'test.schoolRawData', to: 'school.schoolRawData'})" |   mongo --username admin --password admin --authenticationDatabase admin




}

up() {
  echo "Starting Airbyte..."
  docker-compose -f docker-compose-airbyte.yaml --env-file ./.env.airflow down
  docker-compose -f docker-compose-airbyte.yaml --env-file ./.env.airbyte up -d

  echo "Starting Airflow..."
  docker-compose -f docker-compose-airflow.yaml --env-file ./.env.airflow down
  docker-compose -f docker-compose-airflow.yaml --env-file ./.env.airflow up -d
  docker-compose -f docker-compose-airflow.yaml --env-file ./.env.airflow run airflow-webserver airflow connections add 'Update_snowflake_database' --conn-uri 'airbyte://host.docker.internal:8000'
  echo "Access Airflow at http://localhost:8080 to kick off your Airbyte sync DAG."


}
build_up() {
  echo "Building then Starting Airbyte..."
  docker-compose -f docker-compose-airbyte.yaml --env-file ./.env.airflow down
  docker-compose -f docker-compose-airbyte.yaml --env-file ./.env.airflow up --build -d

  echo "Building then Starting Airflow..."
  docker-compose -f docker-compose-airflow.yaml --env-file ./.env.airflow down
  docker-compose -f docker-compose-airflow.yaml --env-file ./.env.airflow up --build -d
  echo "Access Airflow at http://localhost:8080 to kick off your Airbyte sync and monitor your DAG."
  echo "Access Airbyte at http://localhost:8000 to see your existing connections and logs."
}

down() {
  echo "Stopping Airbyte..."
  docker-compose -f docker-compose-airbyte.yaml --env-file ./.env.airflow down
  echo "Stopping Airflow..."
  docker-compose -f docker-compose-airflow.yaml --env-file ./.env.airflow down
}

case $1 in
  up)
    up
    ;;
  down)
    down
    ;;
  install)
    install
    ;;
  *)
    echo "Usage: $0 {up|down}"
    ;;
esac
