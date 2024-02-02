#!/bin/bash

# Define colors for better readability
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null ; then
    echo -e "${YELLOW}Error: Docker is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null ; then
    echo -e "${YELLOW}Error: Docker Compose is not installed. Please install it first.${NC}"
    exit 1
fi

# Specify the directory of the compose.yml file (change this to your desired directory)
COMPOSE_DIR="/opt/shield"

# Check if the directory exists
if [ ! -d "$COMPOSE_DIR" ]; then
    echo -e "${YELLOW}Error: The specified directory does not exist. Exiting with code 1.${NC}"
    exit 1
fi

# Check if there are running containers
if docker compose -f "$COMPOSE_DIR"/compose.yml ps --quiet > /dev/null 2>&1; then
    echo -e "${YELLOW}Stopping and removing existing containers...${NC}"
    docker compose -f "$COMPOSE_DIR"/compose.yml down > /dev/null 2>&1

    # Check the exit status of the 'docker compose down' command
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Existing containers stopped and removed successfully.${NC}"
    else
        echo -e "${YELLOW}Error: Failed to stop and remove existing containers. Exiting with code 1.${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}No running containers found. Exiting with code 1.${NC}"
    exit 1
fi

# Start containers in the background
echo -e "${YELLOW}Starting containers in the background...${NC}"
docker compose -f "$COMPOSE_DIR"/compose.yml up -d > /dev/null 2>&1

# Check if containers started successfully
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Containers started successfully.${NC}"
else
    echo -e "${YELLOW}Error: Failed to start containers. Exiting with code 1.${NC}"
    exit 1
fi
