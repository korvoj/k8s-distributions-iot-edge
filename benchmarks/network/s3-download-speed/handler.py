import boto3
from time import time
import json
from botocore.client import Config
import uuid

s3_client = boto3.client('s3', endpoint_url='<S3_DOWNLOAD_SPEED_S3_ENDPOINT>',
                   aws_access_key_id='<S3_DOWNLOAD_SPEED_S3_ACCESS_KEY>',
                   aws_secret_access_key='<S3_DOWNLOAD_SPEED_S3_SECRET_KEY>',
                   config=Config(signature_version='s3v4'),
                   region_name='<S3_DOWNLOAD_SPEED_S3_REGION_NAME>')


def handle(event, context):
    input_bucket = event.query['input_bucket']
    object_key = event.query['object_key']
    output_bucket = event.query['output_bucket']
    start_time = float(event.query['start_time'])
    request_uuid = event.query['uuid']

    new_name = object_key+str(uuid.uuid4())

    path = '/tmp/'+new_name

    start = time()
    s3_client.download_file(input_bucket, object_key, path)
    download_time = time() - start

    start = time()
    s3_client.upload_file(path, output_bucket, new_name)
    upload_time = time() - start

    return {
        "statusCode": 200,
        "body": {
            "download_time": download_time,
            "upload_time": upload_time,
            "start_time": start_time,
            "uuid": request_uuid,
            "test_name": "s3-download-speed"
            }
    }
