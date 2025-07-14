#!/usr/bin/bash

# Variables
HOST=$1
SOURCE_FOLDER=$(pwd)
NEW_AVAILABLE_SITE_FILE=$HOST.conf
GATEWAY_FOR_SITE_FILE=gunicorn-$HOST.service
ARGS=($@)

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
setup_nginx(){
    CONF_TO_EDIT="$1"
    POSTFIX="$2"
    sed "s/HOST_PLACE_SETUP/$HOST/g" $CONF_TO_EDIT | sed "s/USER_PLACE_SETUP/$USER/g" > $POSTFIX--$NEW_AVAILABLE_SITE_FILE 
    status "Edited file {{$CONF_TO_EDIT}} and created new one {{$POSTFIX--$NEW_AVAILABLE_SITE_FILE}}" "Could not edit file {{$CONF_TO_EDIT}}"

    echo " <<< MOVE AND LINK NEW NGINX CONFIGURATION >>>"
    sudo mv $POSTFIX--$NEW_AVAILABLE_SITE_FILE /etc/nginx/sites-available/ > /dev/null 2>&1
    status "Moved a file {{$POSTFIX--$NEW_AVAILABLE_SITE_FILE}} into /etc/nginx/sites-available"
    if [ ! -e /etc/nginx/sites-enabled/$POSTFIX--$NEW_AVAILABLE_SITE_FILE ]; then
        sudo ln -s /etc/nginx/sites-available/$POSTFIX--$NEW_AVAILABLE_SITE_FILE /etc/nginx/sites-enabled/$POSTFIX--$NEW_AVAILABLE_SITE_FILE > /dev/null 2>&1
        status "Created a symbolic links from {{/etc/nginx/sites/available/$POSTFIX--$NEW_AVAILABLE_SITE_FILE}} to {{/etc/nginx/sites-enabled/$POSTFIX--$NEW_AVAILABLE_SITE_FILE}}" "Could not create a symbolic link"
    else
        echo "  INFO: Symbolic link already exists {{/etc/nginx/sites-enabled/$POSTFIX--$NEW_AVAILABLE_SITE_FILE}}"
    fi
}

echo "<<< START SERVER SETUP PROCCESS >>>"

if [ -z $1 ]; then
    echo "  INFO: You need to specify your host name like website.com or staging.website.com"
    echo "<<< END SERVER SETUP PROCCESS >>>"
    exit 1
fi

echo " <<< SETUP THE NGINX >>>"

SITES_AVAILABLE=("http--$NEW_AVAILABLE_SITE_FILE" "https--$NEW_AVAILABLE_SITE_FILE")
for available_site in ${SITES_AVAILABLE[@]}; do
    if [ -e /etc/nginx/sites-available/$available_site ]; then
        sudo rm /etc/nginx/sites-available/$available_site
        sudo rm /etc/nginx/sites-enabled/$available_site
    fi
done

if has_param 'on_https'; then 
    sudo $SOURCE_FOLDER/../venv/bin/certbot certonly --nginx --agree-tos -q -d $HOST
    status "Obtained, register and place the certificates" "Failed to obtain, register and place the certificates"
    setup_nginx "nginx-server-on_https-301.conf" "http"
    setup_nginx "nginx-server-on_https.conf" "https"
else
    setup_nginx "nginx-server-http_only.conf" "http"
fi
sudo systemctl unmask nginx 
sudo systemctl restart nginx > /dev/null 2>&1
status "Restart the nginx daemon" "Could not restart the nginx daemon"

echo " <<< SETUP THE GUNICORN >>>"
sed "s/HOST_PLACE_SETUP/$HOST/g" gunicorn.service | sed "s/USER_PLACE_SETUP/$USER/g" > $GATEWAY_FOR_SITE_FILE
status "Edited file {{gunicorn.service}} and created new one {{$GATEWAY_FOR_SITE_FILE}}" "Could not edit file {{gunicorn.service}}"
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