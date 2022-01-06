import boto3
from botocore.client import Config
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import pandas as pd
from time import time
import re
import io


s3_client = boto3.client('s3', endpoint_url='<MODEL_TRAINING_S3_ENDPOINT>',
                   aws_access_key_id='<MODEL_TRAINING_S3_ACCESS_KEY>',
                   aws_secret_access_key='<MODEL_TRAINING_S3_SECRET_KEY>',
                   config=Config(signature_version='s3v4'),
                   region_name='<MODEL_TRAINING_S3_REGION_NAME>')

cleanup_re = re.compile('[^a-z]+')
tmp = '/tmp/'


def cleanup(sentence):
    sentence = sentence.lower()
    sentence = cleanup_re.sub(' ', sentence).strip()
    return sentence


def handle(event, context):
    dataset_bucket = event.query['dataset_bucket']
    dataset_object_key = event.query['dataset_object_key']
    model_bucket = event.query['model_bucket']
    model_object_key = event.query['model_object_key']  # example : lr_model.pk
    start_time = float(event.query['start_time'])
    request_uuid = event.query['uuid']

    obj = s3_client.get_object(Bucket=dataset_bucket, Key=dataset_object_key)
    df = pd.read_csv(io.BytesIO(obj['Body'].read()))

    start = time()
    df['train'] = df['Text'].apply(cleanup)

    tfidf_vector = TfidfVectorizer(min_df=100).fit(df['train'])

    train = tfidf_vector.transform(df['train'])

    model = LogisticRegression()
    model.fit(train, df['Score'])
    latency = time() - start

    model_file_path = tmp + model_object_key
    joblib.dump(model, model_file_path)

    s3_client.upload_file(model_file_path, model_bucket, model_object_key)

    return {
        "statusCode": 200,
        "body": {
            'latency': latency,
            'start_time': start_time,
            'uuid': request_uuid,
            'test_name': 'model-training'
        }
    }
