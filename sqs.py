import boto3
import json

sqs = boto3.resource('sqs')

# Get queue
def createQueue():
    # Create the queue. This returns an SQS.Queue instance
    queue = sqs.create_queue(QueueName='locust', Attributes={'DelaySeconds': '5'})

    # You can now access identifiers and attributes
    print(queue.url)
    print(queue.attributes.get('DelaySeconds'))

def sendMessage(url, region):
    sqs = boto3.client('sqs', region_name=region)
    queue = sqs.get_queue_url(QueueName='locust')
    response = sqs.send_message(QueueUrl=queue['QueueUrl'], MessageBody=url)
