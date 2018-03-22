import boto3
from botocore.exceptions import ClientError
import sys

# regions = ['us-east-1', 'us-west-1', 'ap-south-1']
regions = ['us-west-1']
amis = {'us-east-1': 'ami-43a15f3e', 'us-west-1': 'ami-925144f2', 'ap-south-1': 'ami-0189d76e'}
azs = {'us-east-1': ['us-east-1a', 'us-east-1b', 'us-east-1c'], 'us-west-1': ['us-west-1b', 'us-west-1c'], 'ap-south-1':['ap-south-1a', 'ap-south-1b']}
launch_configuration_name="pywebdev_launch_config"
asg_name="pywebdev_as_group"
InstanceProfile=sys.argv[0]
# 3 Core Concepts
#
# 1. Launch Configuration
# 2. Autoscale Group
# 3. Triggers

# Create SQS Queue

sqs = boto3.resource('sqs')
try:
    queue = sqs.create_queue(QueueName='locust', Attributes={'DelaySeconds': '1'})
except ClientError as e:
    print ("Queue already exists", e)

# Create LCs
for region in regions:
    autoscale_conn = boto3.client('autoscaling',region_name=region)
    # First setup a Launch Configuration
    f = open('./files/userdata.txt')
    try:
        lc = autoscale_conn.create_launch_configuration(LaunchConfigurationName=launch_configuration_name, ImageId=amis[region],
                                    InstanceType='t2.micro', # defaults to m1.small
                                    KeyName='seth',
                                    UserData=f.read(), # Reads userdata.txt
                                    IamInstanceProfile='ec2siz',
                                    SecurityGroups=['default'])
    except ClientError as e:
        print(region, "Launch Configuration {} already exists".format(launch_configuration_name))
        print(e)
        continue

    print(region, ' Launch Configuration Creation Result: ', lc['ResponseMetadata']['HTTPStatusCode'])
    f.close()

# Create ASGs
for region in regions:
    autoscale_conn = boto3.client('autoscaling',region_name=region)
    # Now we have a Launch Configuration and an ELB.  Create and launch the AutoScalingGroup
    try:
        ag = autoscale_conn.create_auto_scaling_group(AutoScalingGroupName=asg_name,
                                  AvailabilityZones=azs[region],
                                  LaunchConfigurationName=launch_configuration_name, MinSize=1, MaxSize=1)
    except ClientError as e:
        print(region, 'ASG {} already exists'.format(asg_name))
        continue

    print(region, 'Auto Scaling Group Creation Result: ', ag['ResponseMetadata']['HTTPStatusCode'])
