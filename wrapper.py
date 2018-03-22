import time
import boto3
import sys

queuename = sys.argv[0]

queue = sqs.get_queue_by_name(QueueName='locust')

for message in queue.receive_messages():
    url = message.body
    print(url)
