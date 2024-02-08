#!/bin/bash

# Define color codes
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
NC="\033[0m" # No Color

instDir="/opt/shield/scripts"
downloadURL="https://raw.githubusercontent.com/Shield-Cyber/ShieldCyber-REST-API/main/scripts/"

ensure_directory() {
    local directory=$1

    if [ ! -d "$directory" ]; then
        mkdir -p "$directory"
        echo -e "${YELLOW}$directory created.${NC}"
    fi
}

download_file() {
    local url=$downloadURL$1
    local filename=$(basename "$url")
    local filepath="$instDir/$filename"

    ensure_directory "$instDir"

    echo -e "${YELLOW}Downloading $filename to $instDir... ${NC}"
    curl -sS "$url" -o "$filepath"
    echo -e "${GREEN}$filename downloaded to $instDir! ${NC}"
}

echo -e "${YELLOW}Downloading Shield Executable ${NC}"
curl -sSo /usr/local/bin/shield https://raw.githubusercontent.com/Shield-Cyber/ShieldCyber-REST-API/main/scripts/shield
chmod +x /usr/local/bin/shield
echo -e "${GREEN}Shield Executable Downloaded! ${NC}"

echo -e "${YELLOW}Downloading Shield Helper Scripts ${NC}"
download_file full-install.sh
download_file vuln-update.sh
download_file full-update.sh
