#!/bin/sh
set -x
gpio -g write 22 0
sleep 0.1
gpio -g write 22 1
