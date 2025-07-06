#!/usr/bin/bash

# Variables
REPO="https://github.com/DmRafaule/DjangoDeploymentTest.git"
HOST="beget-django-deployment-test.online"

# Notes
#> /dev/null 2>&1  -- means that any command output either successfull or failed will be suppressed and hided

# Helper functions
status() {
    if [ $? -eq 0 ]; then
        echo $1
    else
        echo $2
        exit
    fi
}


echo "START DEPLOY PROCCESS"

# Create a project structure
ROOT_SITE_FOLDER=/home/$USER/sites/www.$HOST
mkdir -p $ROOT_SITE_FOLDER > /dev/null 2>&1
status "Successfully created folder -> $ROOT_SITE_FOLDER" "Failed to create new folder -> $ROOT_SITE_FOLDER"
# Create a virtual environment for python
cd $ROOT_SITE_FOLDER > /dev/null 2>&1
status "Now in -> $ROOT_SITE_FOLDER" "Could not to enter -> $ROOT_SITE_FOLDER"
if [ -d "$ROOT_SITE_FOLDER/venv" ]; then
    echo "Virtual environment already exist"
else 
    python -m venv venv
    status "Successfully created a virtual environment for project" "Failed to create a virtual environment for project"
fi
# Download a remote repository
if [ -d "$ROOT_SITE_FOLDER/.git" ]; then
    echo "Git repo already persist"
else
    git 
fi