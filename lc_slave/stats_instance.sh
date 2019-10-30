#!/bin/bash

DOCKER_STATS_CMD=`docker stats $1 --no-stream --format "table {{.MemPerc}} {{.CPUPerc}}"`
echo "${DOCKER_STATS_CMD}"
