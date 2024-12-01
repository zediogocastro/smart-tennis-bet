#!/bin/bash

run_containers() {
    echo "Starting the containers..."
    docker-compose up
    echo "Containers are up and running!"
    # Step 2: Run the database setup and ETL scripts
    docker-compose exec web python create_tables.py
    docker-compose exec web python etl.py

    # Add enricher
    echo "Running the data enricher..."
    docker-compose exec web python src/data_enricher.py
    echo "Data enrichment complete!"
}

list_containers() {
    echo "Listing running containers..."
    docker ps  # Show the running Docker containers
}

stop_containers() {
    echo "Stopping the containers..."
    docker-compose down  # Stop all running containers
    echo "Containers have been stopped."
}

# Parse the command-line arguments
if [ "$1" == "--run" ]; then
    run_containers
elif [ "$1" == "--top" ]; then
    list_containers
elif [ "$1" == "--stop" ]; then
    stop_containers
else
    echo "Invalid argument. Use one of the following:"
    echo "--run   : Run containers"
    echo "--top   : List running containers"
    echo "--stop  : Stop running containers"
fi