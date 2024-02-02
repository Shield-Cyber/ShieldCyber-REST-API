#!/bin/bash

# Define color codes
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
NC="\033[0m" # No Color

# Set the directory of the compose.yml file
COMPOSE_DIR="/opt/shield"

# Check if the directory exists
if [ ! -d "$COMPOSE_DIR" ]; then
  echo -e "${RED}Error: Directory not found ${COMPOSE_DIR}${NC}"
  exit 1
fi

echo -e "${YELLOW}Updating Vulnerabikity Database ${NC}"

# Run docker-compose with the specified directory
docker compose -f "${COMPOSE_DIR}/compose.yml" up -d > /dev/null 2>&1

if [ $? -eq 0 ]; then
  echo -e "${GREEN}Shield Scanner Vulnerability Database Update Succeeded ${NC}" 
  echo -e "${YELLOW}Please allow up to 30 minutes for the vulnerability database to update before starting new scans. ${NC}"
else
  echo -e "${RED}Shield Scanner Startup Failed ${NC}"
  echo -e "${YELLOW}Reach out to Shield team for assistance in manual installation. ${NC}"
fi
