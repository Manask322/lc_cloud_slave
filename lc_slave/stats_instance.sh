#!/bin/bash

DOCKER_STATS_CMD=`docker stats $1 --no-stream --format "table {{.MemPerc}} {{.CPUPerc}}" | awk 'NR==2{print}'`
echo "${DOCKER_STATS_CMD}"
