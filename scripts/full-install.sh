#!/bin/bash

instDir="/opt/shield"

# Define color codes
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
NC="\033[0m" # No Color

# Function to download a file to the specified directory
download_file() {
    local url=$1
    local filename=$(basename "$url")
    local filepath="$instDir/$filename"

    echo -e "${YELLOW}Downloading $filename to $instDir... ${NC}"
    curl -S "$url" -o "$filepath"
    echo -e "${GREEN}$filename downloaded to $instDir! ${NC}"

    echo "$filepath"
}

# Function to check if a directory exists and ask to overwrite it
ensure_directory() {
    local directory=$1

    if [ -d "$directory" ]; then
        read -p "$(echo -e "${YELLOW}$directory already exists. Do you want to overwrite it? (y/N): ${NC}")" overwrite_choice

        if [ "$overwrite_choice" == "y" ]; then
            rm -rf "$directory"
            echo -e "${YELLOW}$directory overwritten.${NC}"
        else
            echo -e "${YELLOW}Skipping overwrite.${NC}"
            exit 1
        fi
    else
        mkdir -p "$directory"
        echo -e "${YELLOW}$directory created.${NC}"
    fi
}

echo -e "${YELLOW}Waiting 10 Seconds Before Starting Installation ${NC}"
sleep 10

# Check and ask to overwrite installation directory
ensure_directory "$instDir"

echo -e "${YELLOW}Installing Shield Scanner and its Dependencies ${NC}"

# Install Docker
echo -e "${YELLOW}Removing existing Docker installations... ${NC}"
sudo apt-get remove -y docker docker-engine docker.io containerd runc

echo -e "${YELLOW}Updating package repositories... ${NC}"
sudo apt-get update

echo -e "${YELLOW}Installing necessary dependencies... ${NC}"
sudo apt-get install -y ca-certificates curl gnupg

echo -e "${YELLOW}Setting up Docker GPG key... ${NC}"
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo -e "${YELLOW}Configuring Docker repository... ${NC}"
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo -e "${YELLOW}Updating package repositories... ${NC}"
sudo apt-get update

echo -e "${YELLOW}Installing Docker... ${NC}"
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose

# Check if Docker installation was successful
if command -v docker &> /dev/null ; then
    echo -e "${GREEN}Docker Installed successfully! ${NC}"
else
    echo -e "${RED}Docker installation failed. Exiting with code 1.${NC}"
    exit 1
fi

# Download Compose File
compose_filepath=$(download_file "https://raw.githubusercontent.com/Shield-Cyber/ShieldCyber-REST-API/main/compose.yml")

# Check if .env file exists
env_filepath="$instDir/.env"
if [ -f "$env_filepath" ]; then
    # .env file exists, ask user if they want to update the password
    read -p "$(echo -e "${YELLOW}Installation Found: Do you want to update the password? (y/N): ${NC}")" update_choice

    if [ "$update_choice" == "y" ]; then
        read -sp "Enter Shield Scanner / API Admin Password: " password
        echo -e "\nPASSWORD=$password" > "$env_filepath"
        echo -e "\n${GREEN}Password updated successfully.${NC}"
    else
        echo -e "\n${YELLOW}Skipping password update.${NC}"
    fi
else
    # .env file doesn't exist, create and update it
    read -sp "Enter Shield Scanner / API Admin Password: " password
    echo -e "\nPASSWORD=$password" > "$env_filepath"
fi

# Start Shield Scanner
echo -e "\n${GREEN}Starting Shield Scanner${NC}"
echo -e "${YELLOW}This may take a moment the first time.${NC}"

docker compose -f /opt/shield/compose.yml up -d > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Shield Scanner Startup Complete ${NC}" 
    echo -e "${YELLOW}Please allow up to 30 minutes for the vulnerability database to download before setting up and starting scans. ${NC}"
else
    echo -e "${RED}Shield Scanner Startup Failed ${NC}"
    echo -e "${YELLOW}Reach out to Shield team for assistance in manual installation. ${NC}"
fi