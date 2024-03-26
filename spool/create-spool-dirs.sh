#!/bin/sh

# Create the spool directories. Make sure they have the correct permissions.

. ../secrets/.env
mkdir -p ${TRIGGER_SPOOL_DIRECTORY}
mkdir -p ${IMAGE_SPOOL_DIRECTORY}
mkdir -p ${NOTIFY_SPOOL_DIRECTORY}
