#!/bin/bash

# Exit on any errors
set -e

# Default directory and service settings
instDir="/opt/shield"
serviceName="ShieldCyber.Agent.Shield"
serviceFile="$serviceName.service"
servicePath="/etc/systemd/system/$serviceFile"
downloadURL="https://shieldcyberstoregen.blob.core.windows.net/sc-shield-services/shield-linux.zip"

# Default flags
subscriptionID=""
locationName=""
subscriptionAPIKey=""

# Help message
usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -s    Subscription ID"
    echo "  -l    Location Name"
    echo "  -k    Subscription API Key"
    echo "  -h    Display this help message"
    exit 1
}

# Parse command line options
while getopts ":s:l:k:h" opt; do
    case $opt in
        s ) subscriptionID=$OPTARG ;;
        l ) locationName=$OPTARG ;;
        k ) subscriptionAPIKey=$OPTARG ;;
        h ) usage ;;
        ? ) echo "Invalid Option: -$OPTARG" >&2; usage ;;
        : ) echo "Option -$OPTARG requires an argument." >&2; usage ;;
    esac
done

# Stop, disable, and remove existing service
systemctl stop $serviceName
systemctl disable $serviceName
rm -f $servicePath
systemctl daemon-reload
systemctl reset-failed

# Back up the current appsettings.json
echo "Backing up current appsettings.json..."
cp $instDir/appsettings.json $instDir/appsettings.json.bak

# Download and extract new service files
echo "Downloading new service files..."
curl -sL -o shield-linux.zip "$downloadURL"

unzip -o shield-linux.zip -d $instDir
rm -f shield-linux.zip

# Restore the original appsettings.json if no flags are provided, otherwise update
if [ -n "$subscriptionID" ] || [ -n "$locationName" ] || [ -n "$subscriptionAPIKey" ]; then
    echo "Updating appsettings.json with new settings..."
    jq --arg s "$subscriptionID" --arg l "$locationName" --arg k "$subscriptionAPIKey" \
       '.AppSettings.SubscriptionId = $s | .AppSettings.LocationName = $l | .AppSettings.SubscriptionApiKey = $k' \
       $instDir/appsettings.json > $instDir/appsettings.tmp.json
    mv $instDir/appsettings.tmp.json $instDir/appsettings.json
else
    echo "Restoring original appsettings.json..."
    cp $instDir/appsettings.json.bak $instDir/appsettings.json
fi

# Clean up backup file
rm -f $instDir/appsettings.json.bak

# Setup and start new service
echo "Setting up new service..."
chmod +x $instDir/$serviceName
cp $instDir/$serviceFile $servicePath
systemctl daemon-reload
systemctl enable $serviceName
systemctl start $serviceName
echo "Service setup complete."

exit 0