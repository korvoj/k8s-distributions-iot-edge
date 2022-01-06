import subprocess
import uuid

tmp = '/tmp'

"""
dd - convert and copy a file
man : http://man7.org/linux/man-pages/man1/dd.1.html
Options
 - bs=BYTES
    read and write up to BYTES bytes at a time (default: 512);
    overrides ibs and obs
 - if=FILE
    read from FILE instead of stdin
 - of=FILE
    write to FILE instead of stdout
 - count=N
    copy only N input blocks
"""


def handle(event, context):
    bs = 'bs='+event.query['bs']
    count = 'count='+event.query['count']
    identifier = str(uuid.uuid4())

    start_time = float(event.query['start_time'])
    request_uuid = event.query['uuid']

    result = -1
    out_fd = open(tmp + f'/io_write_logs-{identifier}', 'w')
    dd = subprocess.Popen(['dd', 'if=/dev/zero', f'of=/tmp/out-{identifier}', bs, count, 'oflag=dsync'], stderr=out_fd)
    dd.communicate()

    subprocess.check_output(['ls', '-alh', tmp])

    with open(tmp + f'/io_write_logs-{identifier}') as logs:
        result = str(logs.readlines()[2]).replace('\n', '')
        return {
            "statusCode": 200,
            "body": {
            'message': result,
            'start_time': start_time,
            'uuid': request_uuid,
            'test_name': 'dd',
            'bs': event.query['bs'],
            'count': event.query['count']
        }
        }

    return {
        "statusCode": 500,
        "body": f'{result}'
    }
