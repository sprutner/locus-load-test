
import time
import boto3
import sys
import subprocess

sqs = boto3.resource('sqs')
queuename = sys.argv[0]

queue = sqs.get_queue_by_name(QueueName='locust')

for message in queue.receive_messages():
    url = message.body
    print(url)
    subprocess.call('locust --no-web -c 10000 -r 100 --host {} --csv=foobar'.format(url), shell=True)
