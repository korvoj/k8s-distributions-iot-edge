import math
from time import time
import json

def float_operations(n):
    start = time()
    for i in range(0, n):
        sin_i = math.sin(i)
        cos_i = math.cos(i)
        sqrt_i = math.sqrt(i)
    latency = time() - start
    return latency

def handle(event, context):
    number = int(event.query['number'])
    start_time = float(event.query['start_time'])
    request_uuid = event.query['uuid']
    latency = float_operations(number)
    return {
        "statusCode": 200,
        "body": {
            'latency': latency,
            'start_time': start_time,
            'uuid': request_uuid,
            'test_name': 'float-operation',
            'number': number
        }
    }
