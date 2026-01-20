#!/bin/bash

# Azure ARM Template Deployment Script
# This script deploys the main1.json ARM template to Azure

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting Azure ARM template deployment..."

# Check if az cli is installed
if ! command -v az &> /dev/null; then
    echo "Error: Azure CLI is not installed. Please install it first."
    exit 1
fi

# Download the ARM template from GitHub
echo "Downloading ARM template..."
curl -sL https://raw.githubusercontent.com/gcharanteja/unilogger/main/main1.json -o main1.json

if [ ! -f "main1.json" ]; then
    echo "Error: Failed to download main1.json"
    exit 1
fi

echo "ARM template downloaded successfully."

# Login to Azure (optional, depending on your environment)
# Uncomment the next line if you need to login
# az login

# Get the first resource group from the subscription
echo "Getting resource group..."
RESOURCE_GROUP=$(az group list --query "[0].name" -o tsv)

if [ -z "$RESOURCE_GROUP" ]; then
    echo "Error: No resource groups found in the subscription."
    exit 1
fi

echo "Using resource group: $RESOURCE_GROUP"

# Deploy the ARM template
echo "Deploying ARM template..."
az deployment group create \
  --resource-group "$RESOURCE_GROUP" \
  --template-file main1.json

echo "Deployment completed successfully!"

# Show the public IP of the VM
VM_PUBLIC_IP=$(az vm list-ip-addresses --name learnvm2 --resource-group "$RESOURCE_GROUP" --query "virtualMachine.network.publicIpAddresses[0].ipAddress" -o tsv)
echo "VM Public IP Address: $VM_PUBLIC_IP"

echo "You can connect to the VM using:"
echo "ssh linuxuser@$VM_PUBLIC_IP"