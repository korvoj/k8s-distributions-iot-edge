#!/bin/bash

set -m

STARTING_LOAD=4

I_START=0
I_INCREMENT=4
I_MAX=48

echo -n "$STARTING_LOAD" > current_load

./pod_num_replicas.py & ./hpa-autoscaling.sh $I_START $I_INCREMENT $I_MAX && fg
