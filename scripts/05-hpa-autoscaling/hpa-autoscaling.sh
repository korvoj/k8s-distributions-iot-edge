#!/bin/bash

STEP_DURATION=5m
START=$1
INCREMENT=$2
LIMIT=$3
OPENFAAS_URL=$4

for i in $(seq $START +$INCREMENT $LIMIT)
# for i in $(seq $START -$INCREMENT $LIMIT)
# for i in 8 1 20 4 40 24 1 4 16 1 36 32
do
  if [ $i -eq 0 ]
  then
    echo "skipping..."
  else
    if [ $i -ne $START ]
    then
      echo -n "$i" > current_load
    fi
    echo "New test with concurrency $i for $STEP_DURATION"
    hey -z $STEP_DURATION -c $i -q 1  -t 0 -o csv -m GET "https://$OPENFAAS_URL/function/float-operation?number=100000&uuid=$(uuidgen)&start_time=$(date +%s)" > float-operation-scaling-c$i-q1-t$STEP_DURATION.csv
  fi
done

echo -n "0" > current_load
