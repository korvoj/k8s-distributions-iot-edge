import boto3
import uuid
from time import time
import cv2
from botocore.client import Config


s3_client = boto3.client('s3', endpoint_url='<VIDEO_PROCESSING_S3_ENDPOINT>',
                   aws_access_key_id='<VIDEO_PROCESSING_S3_ACCESS_KEY>',
                   aws_secret_access_key='<VIDEO_PROCESSING_S3_SECRET_KEY>',
                   config=Config(signature_version='s3v4'),
                   region_name='<VIDEO_PROCESSING_S3_REGION_NAME>')


tmp = "/tmp/"
FILE_NAME_INDEX = 0
FILE_PATH_INDEX = 2


def video_processing(object_key, video_path):
    file_name = object_key.split(".")[FILE_NAME_INDEX]
    result_file_path = tmp+file_name+f'-output-{str(uuid.uuid4())}.avi'

    video = cv2.VideoCapture(video_path)

    width = int(video.get(3))
    height = int(video.get(4))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(result_file_path, fourcc, 20.0, (width, height))

    start = time()
    while video.isOpened():
        ret, frame = video.read()

        if ret:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            tmp_file_path = tmp+'tmp.jpg'
            cv2.imwrite(tmp_file_path, gray_frame)
            gray_frame = cv2.imread(tmp_file_path)
            out.write(gray_frame)
        else:
            break

    latency = time() - start

    video.release()
    out.release()
    return latency, result_file_path


def handle(event, context):
    input_bucket = event.query['input_bucket']
    object_key = event.query['object_key']
    output_bucket = event.query['output_bucket']

    start_time = float(event.query['start_time'])
    request_uuid = event.query['uuid']

    download_path = tmp+'{}{}'.format(uuid.uuid4(), object_key)

    s3_client.download_file(input_bucket, object_key, download_path)

    latency, upload_path = video_processing(object_key, download_path)

    s3_client.upload_file(upload_path, output_bucket, upload_path.split("/")[FILE_PATH_INDEX])

    return {
        "statusCode": 200,
        "body": {
            'latency': latency,
            'start_time': start_time,
            'uuid': request_uuid,
            'test_name': 'video-processing'
        }
    }
