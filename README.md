# Kubernetes Distributions for the Edge: Serverless Performance Evaluation



This repository contains complementary data for the paper titled Kubernetes Distributions for the Edge: Serverless Performance Evaluation (*Kjorveziroski, V., Filiposka, S. Kubernetes distributions for the edge: serverless performance evaluation. J Supercomput (2022). https://doi.org/10.1007/s11227-022-04430-6*).

Both the source code and raw data results are available.

The tests have been adapted from the FunctionBench benchmarking suite, available on [kmu-bigdata/serverless-faas-workbench](https://github.com/kmu-bigdata/serverless-faas-workbench) and described in:

- _Jeongchul Kim and Kyungyong Lee, 'Function Bench : A Suite of Workloads for Serverless Cloud Function Service',
  IEEE International Conference on Cloud Computing 2019, 07/2019 [pdf](https://kimjeongchul.github.io/assets/paper/FunctionBench%20-%20A%20Suite%20of%20Workloads%20for%20Serverless%20Cloud%20Function%20Service.pdf)_
- _Jeongchul Kim and Kyungyong Lee, 'Practical Cloud Workloads for Serverless FaaS, ACM Symposium on Cloud Computing 2019, 11/2019_ [pdf](https://dl.acm.org/citation.cfm?id=3365439)

The `scripts` directory contains the shell scripts used to automate the tests. The [hey](https://github.com/rakyll/hey) tool is used for all benchmarks. To measure the number of active containers at a given point in time, a custom Python script is provided titled `pod_num_replicas.py`. Before running this script ensure that an appropriate `~/.kube/config` exists with valid credentials to access a given Kubernetes cluster.

The `data` directory contains the output CSV files for each tested Kubernetes distribution. Each CSV files has the following columns (description taken from [hey pull request #126](https://github.com/rakyll/hey/pull/126/files)):

- `response-time` - Total time taken for request (in seconds)
- `DNS+dialup` - Time taken to establish the TCP connection (in seconds)
- `DNS` - Time taken to do the DNS lookup (in seconds)
- `Request-write` - Time taken to write full request (in seconds)
- `Response-delay` - Time taken to first byte received (in seconds)
- `Response-read` - Time taken to read full response (in seconds)
- `status-code` - HTTP status code of the response (e.g. 200)
- `offset` - The time since the start of the benchmark when the request was started. (in seconds)

Note that the results in the `pod_startup_times` subfolder for the `01-cold-start` tests deviate from this schema. These files meassure the time required for a container to become ready once it has been scheduled on a given Kubernetes node. The columns are:

- `id` - unique id for the meassurement, generated randomly as an UUID4.
- `pod_name` - the name of the scheduled pod in the format `$TEST_NAME-random-id`
- `time_scheduled` - UTC time when the container was scheduled
- `time_ready` - UTC time when the container became ready
- `app` - the name of the function being tested
- `date_added` - UTC time when the record has been added to the database
- `test_batch` - batch when the record has been added, denoting the Kubernetes distribution and the run. Allows pausing and resuming of the benchmarks.
- `delay` - the difference between the `time_ready` and the `time_scheduled` columns (the time required for the container to be ready to serve requests once it has been scheduled on a given node)

The `float-operation-scaling.csv` results present in each subfolder for the `05-hpa-autoscaling` runs also have a custom schema:

- `test_name` - the name of the function being tested
- `replicas` - the number of replicas at the time when the entry is recorded
- `timestamp` - UTC timestamp when the record is made
- `load` - expected concurrent load

All the charts used in the paper have been generated using the code available in the Jupyter notebook present in this repository - `k8s-distributions-iot-edge.ipynb`.