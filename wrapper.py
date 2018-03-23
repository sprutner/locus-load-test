#!/usr/bin/python -p

import time
import boto3
import sys
import subprocess
import json

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='locust')

for message in queue.receive_messages():
    dict = json.loads(message.body)
    subprocess.call('locust --no-web -c {} -r {} --host {} --run-time {} --csv=foobar'.format(dict['users'], dict['hatchrate'], dict['url'], dict['runtime']), shell=True)
