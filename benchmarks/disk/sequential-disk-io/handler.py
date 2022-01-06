from time import time
import subprocess
import os
import json
import uuid

def handle(event, context):
    disk_read_latency = 0
    disk_read_bandwidth = 0

    file_size = int(event.query['file_size'])
    byte_size = int(event.query['byte_size'])
    start_time = float(event.query['start_time'])
    request_uuid = event.query['uuid']

    identifier = str(uuid.uuid4())

    file_write_path = f'/tmp/file-{identifier}'

    start = time()
    with open(file_write_path, 'wb', buffering=byte_size) as f:
        f.write(os.urandom(file_size * 1024 * 1024))
        f.flush()
        os.fsync(f.fileno())
    disk_write_latency = time() - start
    disk_write_bandwidth = file_size / disk_write_latency

    output = subprocess.check_output(['ls', '-alh', '/tmp/'])
    print(output)

    start = time()
    with open(file_write_path, 'rb', buffering=byte_size) as f:
        byte = f.read(byte_size)
        while byte != b"":
            byte = f.read(byte_size)
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
        'test_name': 'sequential-disk-io',
        'file_size': file_size,
        'byte_size': byte_size
    }
    }
