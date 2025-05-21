#!/bin/bash

set -euo pipefail
IFS=$'\n\t'
INFO="INFO: [$(basename "$0")] "

echo "$INFO" "Starting container for jsonifier ..."

HOST_USERID=$(stat -c %u "${INPUT_FOLDER}")
HOST_GROUPID=$(stat -c %g "${INPUT_FOLDER}")
CONTAINER_GROUPNAME=$(getent group | grep "${HOST_GROUPID}" | cut --delimiter=: --fields=1 || echo "")

OSPARC_USER='osparcuser'

if [ "$HOST_USERID" -eq 0 ]; then
    addgroup "$OSPARC_USER" root
else
    if [ -z "$CONTAINER_GROUPNAME" ]; then
        CONTAINER_GROUPNAME=my$OSPARC_USER
        addgroup --gid "$HOST_GROUPID" "$CONTAINER_GROUPNAME"
    else
        echo "group already exists"
    fi

    usermod --append --groups "$CONTAINER_GROUPNAME" "$OSPARC_USER"

    chmod g+w "${INPUT_FOLDER}"
    chgrp --recursive "$CONTAINER_GROUPNAME" "${INPUT_FOLDER}"
    chmod g+w "${OUTPUT_FOLDER}"
    chgrp --recursive "$CONTAINER_GROUPNAME" "${OUTPUT_FOLDER}"
fi

exec gosu "$OSPARC_USER" /docker/jsonifier.bash
