#!/bin/sh

# Create the spool directories. Make sure they have the correct permissions.

# shellcheck source=/dev/null # the secrets file is not in the repository
. ../secrets/.env
mkdir -p "${TRIGGER_SPOOL_DIRECTORY}"
mkdir -p "${IMAGE_SPOOL_DIRECTORY}"
mkdir -p "${NOTIFY_SPOOL_DIRECTORY}"
