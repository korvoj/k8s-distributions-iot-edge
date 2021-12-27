from concurrent.futures.thread import ThreadPoolExecutor
from kubernetes import client, config, watch
import threading
import logging
from datetime import datetime

NAMESPACE = 'openfaas-fn'
FUNCTION_NAME = 'float-operation'
lock = threading.Lock()
REPLICA_COUNT = 0

logpath = f'{FUNCTION_NAME}-scaling.csv'
logger = logging.getLogger('log')
logger.setLevel(logging.INFO)
ch = logging.FileHandler(logpath)
ch.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(ch)


def process_event(_event):
    global REPLICA_COUNT
    if _event['type'] == 'ADDED':
        lock.acquire()
        REPLICA_COUNT += 1
        with open('current_load', 'r') as cf:
            current_load = cf.readline()
            logger.info(
                f'{FUNCTION_NAME}, {REPLICA_COUNT}, {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, {current_load}')
            print(
                f'{FUNCTION_NAME} has {REPLICA_COUNT} replicas - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} and expected load of {current_load}')
        lock.release()
    elif _event['type'] == 'DELETED':
        lock.acquire()
        REPLICA_COUNT -= 1
        with open('current_load', 'r') as cf:
            current_load = cf.readline()
            logger.info(
                f'{FUNCTION_NAME}, {REPLICA_COUNT}, {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, {current_load}')
            print(
                f'{FUNCTION_NAME} has {REPLICA_COUNT} replicas - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} and expected load of {current_load}')
        lock.release()


config.load_kube_config()
v1 = client.CoreV1Api()
w = watch.Watch()
current_resource_version = None

with ThreadPoolExecutor(max_workers=4) as executor:
    while True:
        try:
            if not current_resource_version:
                for event in w.stream(v1.list_namespaced_pod, namespace=NAMESPACE,
                                      label_selector=f'faas_function={FUNCTION_NAME}'):
                    future = executor.submit(process_event, event)
            else:
                print('Continuing from a resource version...')
                for event in w.stream(v1.list_namespaced_pod, namespace=NAMESPACE,
                                      resource_version=current_resource_version,
                                      label_selector=f'faas_function={FUNCTION_NAME}'):
                    future = executor.submit(process_event, event)
        except Exception as e:  # Handle the exact required exception and add counter...
            print('Got timeout, retrying...')
            _result = v1.list_namespaced_pod(namespace='default')
            current_resource_version = _result.metadata.resource_version

