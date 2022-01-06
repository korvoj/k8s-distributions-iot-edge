from time import time
import subprocess
import os
import random
import json
import uuid

def handle(event, context):


    file_size = int(event.query['file_size'])
    byte_size = int(event.query['byte_size'])
    start_time = float(event.query['start_time'])
    request_uuid = event.query['uuid']

    identifier = uuid.uuid4()

    file_write_path = f'/tmp/file-{identifier}'

    block = os.urandom(byte_size)
    total_file_bytes = file_size * 1024 * 1024 - byte_size

    start = time()
    with open(file_write_path, 'wb') as f:
        for _ in range(int(total_file_bytes/byte_size)):
            f.seek(random.randrange(total_file_bytes))
            f.write(block)
        f.flush()
        os.fsync(f.fileno())
    disk_write_latency = time() - start
    disk_write_bandwidth = file_size / disk_write_latency

    output = subprocess.check_output(['ls', '-alh', '/tmp/'])
    print(output)

    start = time()
    with open(file_write_path, 'rb') as f:
        for _ in range(int(total_file_bytes/byte_size)):
            f.seek(random.randrange(total_file_bytes))
            f.read(byte_size)
    disk_read_latency = time() - start
    disk_read_bandwidth = file_size / disk_read_latency

    rm = subprocess.Popen(['rm', '-rf', file_write_path])
    rm.communicate()
    return {
        "statusCode": 200,
        "body": {
        'disk_write_bandwidth':disk_write_bandwidth,
        'disk_write_latency':disk_write_latency,
        'disk_read_bandwidth':disk_read_bandwidth,
        'disk_read_latency':disk_read_latency,
        'start_time': start_time,
        'uuid': request_uuid,
        'test_name': 'random-disk-io',
        'file_size': file_size,
        'byte_size': byte_size
    }
    }


