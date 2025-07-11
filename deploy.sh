#!/usr/bin/bash

# Variables
REPO="https://github.com/DmRafaule/DjangoDeploymentTest.git"
REPO_FOLDER="source"
HOST=$1
ROOT_SITE_FOLDER=/home/$USER/$HOST
SOURCE_FOLDER=$ROOT_SITE_FOLDER/$REPO_FOLDER
WEBSITE_FOLDER=$SOURCE_FOLDER/Website
INIT_SETTINGS_FILE="$(pwd)/Website/settings.json"
ARGS=("--skip-tests" "-s")

# Notes
#> /dev/null 2>&1  -- means that any command output either successfull or failed will be suppressed and hided

# Helper functions
status() {
    if [ $? -eq 0 ]; then
        echo "  OK: $1"
    else
        echo "  ERR: $2"
        exit
    fi
}
# Thanks to https://stackoverflow.com/a/56431189/14551020
has_param() {
    local term="$1"
    shift
    for arg in ${ARGS[@]} ; do
        if [[ $arg == "$term" ]]; then
            return 0
        fi
    done
    return 1
}


echo "<<< START DEPLOY PROCCESS >>>"

if [ -z $1 ]; then
    echo "  INFO: You need to specify your host name like website.com or staging.website.com"
    echo "<<< END DEPLOY PROCCESS >>>"
    exit 1
fi

echo " <<< CREATE A FOLDER STRUCTURE >>>"
# Create a project structure
mkdir -p $ROOT_SITE_FOLDER > /dev/null 2>&1
status "Create a folder  {{$ROOT_SITE_FOLDER}}" "Failed to create a folder {{$ROOT_SITE_FOLDER}}"
cd $ROOT_SITE_FOLDER > /dev/null 2>&1
status "Now in {{$ROOT_SITE_FOLDER}}" "Could not to enter {{$ROOT_SITE_FOLDER}}"
mkdir -p media static > /dev/null 2>&1
status "Successfully created folders  {{media/, static/}}" "Failed to create new folder {{media/, static/}}"

echo " <<< DOWNLOAD A REPOSITORY >>>"
# Download a remote repository if not downloaded already
# Otherwise fetch the repo
if [ -d "$SOURCE_FOLDER/.git" ]; then
    echo "  INFO: Git repository {{$REPO}} already persist"
    cd $SOURCE_FOLDER > /dev/null 2>&1
    status "Now in {{$SOURCE_FOLDER}}" "Could not to enter {{$SOURCE_FOLDER}}"
    git fetch > /dev/null 2>&1
    status "Successfully fetched git repo {{$REPO}}" "Could not fetch the repo {{$REPO}}"
    git pull  > /dev/null 2>&1
    status "Successfully pull diff from git repo {{$REPO}}" "Could not pull diff from the repo {{$REPO}}"
else
    git clone $REPO $REPO_FOLDER > /dev/null 2>&1
    status "Successfully clone a git repo {{$REPO}}" "Could not clone the repo {{$REPO}}"
    cd $SOURCE_FOLDER > /dev/null 2>&1
    status "Now in {{$SOURCE_FOLDER}}" "Could not to enter {{$SOURCE_FOLDER}}"
fi
## Get the current commit of the project
CURRENT_COMMIT=$(git log -n 1 --format=%H)
## Drop all changes made to and for live server
git reset --hard $CURRENT_COMMIT > /dev/null 2>&1
status "Now at {{$CURRENT_COMMIT}} in git repo {{$REPO}}" "Could not reset to latest commit {{$CURRENT_COMMIT}} in git repo {{$REPO}}"

echo " <<< SETUP SETTINGS.JSON FOR PRODUCTION >>>"
# Reconfigure the settings.json file
SETTINGS_FILE="$SOURCE_FOLDER/Website/settings.json"
## Copy default configuration
cp $INIT_SETTINGS_FILE $SETTINGS_FILE
status "Successfully copy {{$INIT_SETTINGS_FILE}} file into {{$SETTINGS_FILE}}" "Failed to copy {{$INIT_SETTINGS_FILE}} file into {{$SETTINGS_FILE}}"
## Change debug mode
jq '.DEBUG = false' $SETTINGS_FILE > tmp.json && mv tmp.json $SETTINGS_FILE 
status "Successfully chage the {{DEBUG}} key in {{$SETTINGS_FILE}}" "Failed to change the {{DEBUG}} key in {{$SETTINGS_FILE}}"
## Change the secret key
NEW_SECRET_KEY=\"$( head /dev/urandom | tr -dc A-Za-z0-9 | head -c 64 )\"
jq ".SECRET_KEY = $NEW_SECRET_KEY " $SETTINGS_FILE > tmp.json && mv tmp.json $SETTINGS_FILE
status "Successfully chage the {{SECRET_KEY}} key in {{$SETTINGS_FILE}}" "Failed to change the {{SECRET_KEY}} key in {{$SETTINGS_FILE}}"
## Change allowed hosts
ALLOWED_HOST=\"$HOST\"
jq ".ALLOWED_HOSTS[0] = $ALLOWED_HOST " $SETTINGS_FILE > tmp.json && mv tmp.json $SETTINGS_FILE
status "Successfully chage the {{ALLOWED_HOSTS}} array in {{$SETTINGS_FILE}}" "Failed to change the {{ALLOWED_HOSTS}} array in {{$SETTINGS_FILE}}"
## Change a stagin server
STAGING_SERVER=\"http://$HOST\"
jq ".STAGING_SERVER = $STAGING_SERVER " $SETTINGS_FILE > tmp.json && mv tmp.json $SETTINGS_FILE
status "Successfully chage the {{STAGING_SERVER}} key in {{$SETTINGS_FILE}}" "Failed to change the {{STAGING_SERVER}} key in {{$SETTINGS_FILE}}"

echo " <<< SETUP VIRTUAL ENVIRONMENT >>>"
# Create a virtual environment for python and update it
cd $ROOT_SITE_FOLDER > /dev/null 2>&1
status "Now in {{$ROOT_SITE_FOLDER}}" "Could not to enter {{$ROOT_SITE_FOLDER}}"
if [ -d "$ROOT_SITE_FOLDER/venv" ]; then
    echo "  INFO: Virtual environment already exist"
else 
    python3 -m venv venv
    status "Successfully created a virtual environment for project" "Failed to create a virtual environment for project"
fi
## Activate the virtual environment
cd $SOURCE_FOLDER > /dev/null 2>&1
status "Now in {{$SOURCE_FOLDER}}" "Could not to enter {{$SOURCE_FOLDER}}"
source ../venv/bin/activate > /dev/null 2>&1
status "Successfully activate the virtial environment" "Failed to activate virtual environment"
pip install -r ./requirements.txt > /dev/null 2>&1
status "Successfully update the virtual environment" "Failed to update virtual environment"

echo " <<< SOFT LINKS >>>"
# Create soft links to media and static folders
cd $WEBSITE_FOLDER > /dev/null 2>&1
status "Now in {{$(pwd)}}" "Could not to enter {{$WEBSITE_FOLDER}}"
if [ ! -d static ]; then
    ln -s ../../static static > /dev/null 2>&1
    status "Successfully create a soft link to {{../../static}} folder" "Failed to create a soft link to {{../../static}} folder"
else
    echo "  INFO: Soft link to {{$ROOT_SITE_FOLDER/static}} already exist"
fi
if [ ! -d media ]; then
    ln -s ../../media media > /dev/null 2>&1
    status "Successfully create a soft link to {{../../media}} folder" "Failed to create a soft link to {{../../media}} folder"
else
    echo "  INFO: Soft link to {{$ROOT_SITE_FOLDER/media}} already exist"
fi



echo " <<< DJANGO PREPARATION >>>"
## Collect statics
python manage.py collectstatic --noinput > /dev/null 2>&1
status "Successfully copied statics files" "Failed to copy statics files"
## Make translations
python manage.py compilemessages > /dev/null 2>&1
status "Successfully compiled translation messages" "Failed to compiled translation messages"
## Make migrations
python manage.py migrate --noinput > /dev/null 2>&1
status "Successfully migrate the database" "Failed to migrate the database"

## Run tests only if params not used (ARGS)
if ! has_param $2; then
    echo "  INFO: Init testing"
    python manage.py test
    status "Passed all tests" "Failed to pass the tests"
fi

echo "<<< END DEPLOY PROCCESS >>>"