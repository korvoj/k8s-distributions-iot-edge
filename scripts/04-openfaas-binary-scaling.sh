#!/bin/bash

hey -z 800s -c 6 -q 1 -t 0 -o csv -m GET "$OPENFAAS_URL/function/float-operation?number=1000&uuid=$(uuidgen)&start_time=$(date +%s)""
