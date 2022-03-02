#!/bin/bash

OPENFAAS_USERNAME='admin'
OPENFAAS_PASSWORD="$1"
OPENFAAS_URL="https://$2"
OPENFAAS_PORT='443'


for test_type in linpack matmul chameleon pyaes float-operation gzip-compression json-dumps-loads model-training image-processing video-processing s3-download-speed iperf3 random-disk-io sequential-disk-io dd
do
  echo "Testing $test_type..."
     if [ $test_type == "linpack" ]; then
       hey -n 20 -c 20 -t 0 -o csv -m GET "$OPENFAAS_URL/function/$test_type?number=5000&uuid=$(uuidgen)&start_time=$(date +%s)" > $test_type-parallel-20-worker-1-replica.csv
     elif [ $test_type == "chameleon" ]; then
       hey -n 20 -c 20 -t 0 -o csv -m GET "$OPENFAAS_URL/function/$test_type?num_of_rows=2000&num_of_cols=2000&uuid=$(uuidgen)&start_time=$(date +%s)" > $test_type-parallel-20-worker-1-replica.csv
     elif [ $test_type == "matmul" ]; then
       hey -n 20 -c 20 -t 0 -o csv -m GET "$OPENFAAS_URL/function/$test_type?number=5000&uuid=$(uuidgen)&start_time=$(date +%s)" > $test_type-parallel-20-worker-1-replica.csv
     elif [ $test_type == "pyaes" ]; then
       hey -n 20 -c 20 -t 0 -o csv -m GET "$OPENFAAS_URL/function/$test_type?length_of_message=1000&num_of_iterations=100&uuid=$(uuidgen)&start_time=$(date +%s)" > $test_type-parallel-20-worker-1-replica.csv
     elif [ $test_type == "float-operation" ]; then
       hey -n 20 -c 20 -t 0 -o csv -m GET "$OPENFAAS_URL/function/$test_type?number=10000000&uuid=$(uuidgen)&start_time=$(date +%s)" > $test_type-parallel-20-worker-1-replica.csv
     elif [ $test_type == "gzip-compression" ]; then
       hey -n 20 -c 20 -t 0 -o csv -m GET "$OPENFAAS_URL/function/$test_type?file_size=50&uuid=$(uuidgen)&start_time=$(date +%s)" > $test_type-parallel-20-worker-1-replica.csv
     elif [ $test_type == "json-dumps-loads" ]; then
       hey -n 20 -c 20 -t 0 -o csv -m GET "$OPENFAAS_URL/function/$test_type?link=http://192.168.85.153:8089/large-file.json&uuid=$(uuidgen)&start_time=$(date +%s)" > $test_type-parallel-20-worker-1-replica.csv
     elif [ $test_type == "model-training" ]; then
       hey -n 20 -c 20 -t 0 -o csv -m GET "$OPENFAAS_URL/function/$test_type?dataset_object_key=reviews10mb.csv&dataset_bucket=benchmarks&model_bucket=benchmarks-results&model_object_key=lr_model.pk&uuid=$(uuidgen)&start_time=$(date +%s)" > $test_type-parallel-20-worker-1-replica.csv
     elif [ $test_type == "image-processing" ]; then
       hey -n 20 -c 20 -t 0 -o csv -m GET "$OPENFAAS_URL/function/$test_type?input_bucket=benchmarks&object_key=image.jpg&output_bucket=benchmarks-results&uuid=$(uuidgen)&start_time=$(date +%s)" > $test_type-parallel-20-worker-1-replica.csv
     elif [ $test_type == "video-processing" ]; then
       hey -n 20 -c 20 -t 0 -o csv -m GET "$OPENFAAS_URL/function/$test_type?input_bucket=benchmarks&output_bucket=benchmarks-results&object_key=SampleVideo_1280x720_10mb.mp4&uuid=$(uuidgen)&start_time=$(date +%s)" > $test_type-parallel-20-worker-1-replica.csv
     elif [ $test_type == "s3-download-speed" ]; then
       hey -n 20 -c 20 -t 0 -o csv -m GET "$OPENFAAS_URL/function/$test_type?input_bucket=benchmarks&object_key=100mb&output_bucket=benchmarks-results&uuid=$(uuidgen)&start_time=$(date +%s)" > $test_type-parallel-20-worker-1-replica.csv
     elif [ $test_type == "iperf3" ]; then
       hey -n 20 -c 20 -t 0 -o csv -m GET "$OPENFAAS_URL/function/$test_type?server_ip=192.168.85.10&server_port=5201&reverse=false&test_time=30s&uuid=$(uuidgen)&start_time=$(date +%s)" > $test_type-parallel-20-worker-1-replica.csv
     elif [ $test_type == "random-disk-io" ]; then
       hey -n 20 -c 20 -t 0 -o csv -m GET "$OPENFAAS_URL/function/$test_type?file_size=100&byte_size=1024&uuid=$(uuidgen)&start_time=$(date +%s)" > $test_type-parallel-20-worker-1-replica.csv
     elif [ $test_type == "sequential-disk-io" ]; then
       hey -n 20 -c 20 -t 0 -o csv -m GET "$OPENFAAS_URL/function/$test_type?file_size=100&byte_size=1024&uuid=$(uuidgen)&start_time=$(date +%s)" > $test_type-parallel-20-worker-1-replica.csv
     elif [ $test_type == "dd" ]; then
       hey -n 20 -c 20 -t 0 -o csv -m GET "$OPENFAAS_URL/function/$test_type?bs=100M&count=1&uuid=$(uuidgen)&start_time=$(date +%s)" > $test_type-parallel-20-worker-1-replica.csv
     fi
  echo "Sleeping for 120s before continuing..."
  sleep 120
done
