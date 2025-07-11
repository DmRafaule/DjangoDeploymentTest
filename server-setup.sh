#!/usr/bin/bash

# Variables
HOST=$1
SOURCE_FOLDER=$(pwd)
NEW_AVAILABLE_SITE_FILE=$HOST.conf
GATEWAY_FOR_SITE_FILE=gunicorn-$HOST.service

# Helper functions
status() {
    if [ $? -eq 0 ]; then
        echo "  OK: $1"
    else
        echo "  ERR: $2"
        exit
    fi
}

echo "<<< START SERVER SETUP PROCCESS >>>"

if [ -z $1 ]; then
    echo "  INFO: You need to specify your host name like website.com or staging.website.com"
    echo "<<< END SERVER SETUP PROCCESS >>>"
    exit 1
fi

echo " <<< SETUP THE NEW SERVERS FILE (nginx web-server and gunicorn gateway server) >>>"
sed "s/HOST_PLACE_SETUP/$HOST/g" nginx-server.conf | sed "s/USER_PLACE_SETUP/$USER/g" > $NEW_AVAILABLE_SITE_FILE 
status "Edited file {{nginx-server.conf}} and created new one {{$NEW_AVAILABLE_SITE_FILE}}" "Could not edit file {{nginx-server.conf}}"
sed "s/HOST_PLACE_SETUP/$HOST/g" gunicorn.service | sed "s/USER_PLACE_SETUP/$USER/g" > $GATEWAY_FOR_SITE_FILE
status "Edited file {{gunicorn.service}} and created new one {{$GATEWAY_FOR_SITE_FILE}}" "Could not edit file {{gunicorn.service}}"

echo " <<< MOVE AND LINK NEW NGINX CONFIGURATION >>>"
sudo mv $NEW_AVAILABLE_SITE_FILE /etc/nginx/sites-available/ > /dev/null 2>&1
status "Moved a file {{$NEW_AVAILABLE_SITE_FILE}} into /etc/nginx/sites-available"
if [ ! -e /etc/nginx/sites-enabled/$NEW_AVAILABLE_SITE_FILE ]; then
    sudo ln -s /etc/nginx/sites-available/$NEW_AVAILABLE_SITE_FILE /etc/nginx/sites-enabled/$NEW_AVAILABLE_SITE_FILE > /dev/null 2>&1
    status "Created a symbolic links from {{/etc/nginx/sites/available/$NEW_AVAILABLE_SITE_FILE}} to {{/etc/nginx/sites-enabled/$NEW_AVAILABLE_SITE_FILE}}" "Could not create a symbolic link"
else
    echo "  INFO: Symbolic link already exists {{/etc/nginx/sites-enabled/$NEW_AVAILABLE_SITE_FILE}}"
fi
sudo systemctl unmask nginx 
sudo systemctl restart nginx > /dev/null 2>&1
status "Restart the nginx daemon" "Could not restart the nginx daemon"

echo " <<< MOVE NEW GUNICORN CONFIGURATION >>>"
cd $SOURCE_FOLDER
status "Now in {{$(pwd)}}" "Could not to enter {{$SOURCE_FOLDER}}"
sudo mv $GATEWAY_FOR_SITE_FILE /etc/systemd/system/$GATEWAY_FOR_SITE_FILE
status "Moved a file {{$GATEWAY_FOR_SITE_FILE}} into {{/etc/systemd/system/$GATEWAY_FOR_SITE_FILE}}" "Could not move a file {{$GATEWAY_FOR_SITE_FILE}} into {{/etc/systemd/system/$GATEWAY_FOR_SITE_FILE}}"
sudo systemctl unmask $GATEWAY_FOR_SITE_FILE
sudo systemctl enable $GATEWAY_FOR_SITE_FILE
status "Enable the {{$GATEWAY_FOR_SITE_FILE}} service" "Could not enable the service {{$GATEWAY_FOR_SITE_FILE}}"
sudo systemctl restart $GATEWAY_FOR_SITE_FILE
status "Start the {{$GATEWAY_FOR_SITE_FILE}} service" "Could not start the service {{$GATEWAY_FOR_SITE_FILE}}"

echo "<<< END SERVER SETUP PROCCESS >>>"