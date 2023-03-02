#!/bin/bash

# Login to your Azure account
az login

# Set your subscription ID
az account set --subscription e593f235-2c99-4cfe-94a8-c3ba29147331

# Get the list of resources and their details
resource_list=$(az resource list --output table)

# Print the resource list to the terminal using jq for formatting
az resource list | jq
