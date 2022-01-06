from time import time
import random
import string
import pyaes

def generate(length):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def handle(event, context):

    length_of_message = int(event.query['length_of_message'])
    num_of_iterations = int(event.query['num_of_iterations'])
    start_time = float(event.query['start_time'])
    request_uuid = event.query['uuid']

    message = generate(length_of_message)
    # 128-bit key (16 bytes)
    KEY = b'\xa1\xf6%\x8c\x87}_\xcd\x89dHE8\xbf\xc9,'
    start = time()

    for loops in range(num_of_iterations):
        aes = pyaes.AESModeOfOperationCTR(KEY)
        ciphertext = aes.encrypt(message)
        aes = pyaes.AESModeOfOperationCTR(KEY)
        plaintext = aes.decrypt(ciphertext)
        aes = None

    latency = time() - start

    return {
        "statusCode": 200,
        "body": {
            'latency': latency,
            'length_of_message': length_of_message,
            'num_of_iterations': num_of_iterations,
            'start_time': start_time,
            'uuid': request_uuid,
            'test_name': 'pyaes'
        }
    }
