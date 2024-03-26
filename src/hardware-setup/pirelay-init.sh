#!/bin/sh
set -x
gpio -g write 22 1
sleep 1
gpio -g mode 22 tri
sleep 1
gpio -g mode 22 out
sleep 1
gpio -g write 22 1
