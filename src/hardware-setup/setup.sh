#!/bin/sh
set -x
gpio && sudo apt-get install wiringpi
SERVICE=pirelay-init
sudo cp -f $SERVICE.service /etc/systemd/system/$SERVICE.service
sudo chmod 644 /etc/systemd/system/$SERVICE.service
sudo systemctl enable $SERVICE
sudo systemctl start $SERVICE
