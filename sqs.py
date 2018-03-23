import boto3
import json
from botocore.exceptions import ClientError

sqs = boto3.resource('sqs')
Q = 'locust'
# Get queue
def createQueue(region):
    sqs = boto3.client('sqs', region_name=region)
    try:
        queue = sqs.create_queue(QueueName=Q, Attributes={'DelaySeconds': '1'})
        print('Queue: {} Created'.format(Q))
    except ClientError as e:
        print ("Queue already exists", e)

def sendMessage(url, region):
    sqs = boto3.client('sqs', region_name=region)
    queue = sqs.get_queue_url(QueueName='locust')
    response = sqs.send_message(QueueUrl=queue['QueueUrl'], MessageBody=url)
