# Source Code for the OpenFaaS Tests

All of the 14 tests have been adapted from the [kmu-bigdata/serverless-faas-workbench](https://github.com/kmu-bigdata/serverless-faas-workbench) repository.

To deploy these functions on an existing OpenFaaS installation, the following parameters have to be changed in the YAML file representing the function's definition:

- `<OPENFAAS_GATEWAY>` – full URL of the OpenFaaS gateway, for example `https://gateway.openfaas.example.com`
- `<TEST_DOCKER_IMAGE>` – container image repository URL where the built Docker image will be uploaded. The `TEST` part needs to be replaced with the name of the test. For example:
    - `<FLOAT_OPERATION_DOCKER_IMAGE>`
    - `<CHAMELEON_DOCKER_IMAGE>`
    - `<IMAGE_PROCESSING_DOCKER_IMAGE>`
    - `<LINPACK_DOCKER_IMAGE>`
    - `<MATMUL_DOCKER_IMAGE>`
    - `<MODEL_TRAINING_DOCKER_IMAGE>`
    - `<PYAES_DOCKER_IMAGE>`
    - `<VIDEO_PROCESSING_DOCKER_IMAGE>`
    - `<DD_DOCKER_IMAGE>`
    - `<GZIP_COMPRESSION_DOCKER_IMAGE>`
    - `<RANDOM_DISK_IO_DOCKER_IMAGE>`
    - `<SEQUENTIAL_DISK_IO_DOCKER_IMAGE>`
    - `<JSON_DUMPS_LOADS_DOCKER_IMAGE>`
    - `<S3_DOWNLOAD_SPEED_DOCKER_IMAGE>`

Some of the tests have additional static parameters that must be changed. These parameters are hard-coded so that the request for invoking the function is simpler.

## Parameters for `image-processing`

- `<IMAGE_PROCESSING_S3_ENDPOINT>` - S3 API Endpoint for the server where the images to be converted are hosted
- `<IMAGE_PROCESSING_S3_ACCESS_KEY>` - S3 Access Key for IAM authentication
- `<IMAGE_PROCESSING_S3_SECRET_KEY>` - S3 Secret Key for IAM authentication
- `<IMAGE_PROCESSING_S3_REGION_NAME>` - S3 Region Name

## Parameters for `model-training`

- `<MODEL_TRAINING_S3_ENDPOINT>` - S3 API Endpoint for the server where the training data is hosted
- `<MODEL_TRAINING_S3_ACCESS_KEY>` - S3 Access Key for IAM authentication
- `<MODEL_TRAINING_S3_SECRET_KEY>` - S3 Secret Key for IAM authentication
- `<MODEL_TRAINING_S3_REGION_NAME>` - S3 Region Name

## Parameters for `video-processing`

- `<VIDEO_PROCESSING_S3_ENDPOINT>` - S3 API Endpoint for the server where the training data is hosted
- `<VIDEO_PROCESSING_S3_ACCESS_KEY>` - S3 Access Key for IAM authentication
- `<VIDEO_PROCESSING_S3_SECRET_KEY>` - S3 Secret Key for IAM authentication
- `<VIDEO_PROCESSING_S3_REGION_NAME>` - S3 Region Name

## Parameters for `s3-download-speed`

- `<S3_DOWNLOAD_SPEED_S3_ENDPOINT>` - S3 API Endpoint for the server where the large binary file is hosted
- `<S3_DOWNLOAD_SPEED_S3_ACCESS_KEY>` - S3 Access Key for IAM authentication
- `<S3_DOWNLOAD_SPEED_S3_SECRET_KEY>` - S3 Secret Key for IAM authentication
- `<S3_DOWNLOAD_SPEED_S3_REGION_NAME>` - S3 Region Name

# Deploying the Functions

Once all of the required parameters outlined above have been replaced with their appropriate values, the following commands can be used to build and deploy the functions:

```bash
export OPENFAAS_URL='<OPENFAAS_GATEWAY>'
faas-cli login --password <OPENFAAS_PASSWORD>
faas-cli up -f <FUNCTION_MANIFEST>.yml --gateway <OPENFAAS_GATEWAY>
```

The source files with which the functions have been invoked during our tests are available in the folder `dataset` in the root of the repository.