from time import time
import gzip
import os
import json
import uuid

def handle(event, context):
    file_size = int(event.query['file_size'])
    start_time = float(event.query['start_time'])
    request_uuid = event.query['uuid']

    file_write_path = f'/tmp/file-{str(uuid.uuid4())}'

    start = time()
    with open(file_write_path, 'wb') as f:
        f.write(os.urandom(file_size * 1024 * 1024))
    disk_latency = time() - start

    with open(file_write_path, 'rb') as f:
        start = time()
        with gzip.open(f'/tmp/result-str{uuid.uuid4()}.gz', 'wb') as gz:
            gz.writelines(f)
        compress_latency = time() - start


    return {
        "statusCode": 200,
        "body": {
            'disk_latency': disk_latency,
            'compress_latency': compress_latency,
            'file_size': file_size,
            'start_time': start_time,
            'uuid': request_uuid,
            'test_name': 'gzip-compression'
        }
    }

