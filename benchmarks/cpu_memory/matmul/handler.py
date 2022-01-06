import numpy as np
from time import time

def matmul(n):
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)

    start = time()
    C = np.matmul(A, B)
    latency = time() - start
    return latency

def handle(event, context):
    number = int(event.query['number'])
    latency = matmul(number)
    start_time = float(event.query['start_time'])
    request_uuid = event.query['uuid']
    return {
        "statusCode": 200,
        "body": {
            'latency': latency,
            'start_time': start_time,
            'uuid': request_uuid,
            'number': number,
            'test_name': 'matmul'
        }
    }
