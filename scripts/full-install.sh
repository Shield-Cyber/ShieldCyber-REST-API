#!/bin/bash

instDir="/opt/shield"
password_flag=false

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

    if [ ! -d "$directory" ]; then
        echo -e "${RED}$directory does not exist. Exiting.${NC}"
        exit 1
    fi
}

# Function to set the password in the .env file
set_password() {
    local password="$1"
    local env_filepath="$instDir/.env"
    echo -e "PASSWORD='$password'" > "$env_filepath"
    echo -e "${GREEN}Password set successfully.${NC}"
}

# Function to detect the OS and install Docker accordingly
install_docker() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
        VERSION=$VERSION_ID
    else
        OS=$(uname -s)
        VERSION=$(uname -r)
    fi

    echo -e "${YELLOW}Detected OS: $OS $VERSION ${NC}"

    case "$OS" in
        *rocky*)
            sudo dnf -y update
            sudo dnf -y install dnf-plugins-core
            sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
            sudo dnf -y install docker-ce docker-ce-cli containerd.io
            ;;
        *debian*|*kali*)
            sudo apt-get -y update
            sudo apt-get -y install apt-transport-https ca-certificates curl gnupg lsb-release
            curl -fsSL https://download.docker.com/linux/$OS/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
            echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/$OS $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
            sudo apt-get -y update
            sudo apt-get -y install docker-ce docker-ce-cli containerd.io
            ;;
        *freebsd*)
            sudo pkg install -y docker
            sudo sysrc docker_enable="YES"
            sudo service docker start
            ;;
        *rhel*)
            sudo yum -y update
            sudo yum -y install yum-utils
            sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
            sudo yum -y install docker-ce docker-ce-cli containerd.io
            ;;
        *suse*)
            sudo zypper refresh
            sudo zypper install -y docker docker-compose
            ;;
        *)
            echo -e "${RED}Unsupported OS. Exiting.${NC}"
            exit 1
            ;;
    esac

    sudo systemctl enable docker
    sudo systemctl start docker
}

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        -P|--password)
            password_flag=true
            password="$2"
            shift
            shift
            ;;
        *)
            shift
            ;;
    esac
done

echo -e "${YELLOW}Waiting 10 Seconds Before Starting Installation ${NC}"
sleep 10

# Check if installation directory exists
ensure_directory "$instDir"

echo -e "${YELLOW}Installing Shield Scanner and its Dependencies ${NC}"

# Install Docker
install_docker

# Check if Docker installation was successful
if command -v docker &> /dev/null ; then
    echo -e "${GREEN}Docker Installed successfully! ${NC}"
else
    echo -e "${RED}Docker installation failed. Exiting with code 1.${NC}"
    exit 1
fi

# Download Compose File
compose_filepath=$(download_file "https://raw.githubusercontent.com/Shield-Cyber/ShieldCyber-REST-API/main/compose.yml")

# Set password if flag is provided
if [ "$password_flag" = true ]; then
    set_password "$password"
else
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
