import boto3

sqs = boto3.resource('sqs')

# Get queue
queue = sqs.get_queue_by_name(QueueName='locust')
def createQueue():
    # Create the queue. This returns an SQS.Queue instance
    queue = sqs.create_queue(QueueName='locust', Attributes={'DelaySeconds': '5'})

    # You can now access identifiers and attributes
    print(queue.url)
    print(queue.attributes.get('DelaySeconds'))

def sendMessage(url):
    response = queue.send_message(MessageBody=url)
