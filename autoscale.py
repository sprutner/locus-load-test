import boto.ec2.autoscale
from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import AutoScalingGroup

regions = ['us-east-1', 'us-west-1', 'ap-south-1']
amis = {'us-east-1': 'ami-43a15f3e', 'us-west-1': 'ami-925144f2', 'ap-south-1': 'ami-0189d76e'}
azs = {'us-east-1': ['us-east-1a', 'us-east-1b', 'us-east-1c'], 'us-west-1': ['us-west-1b', 'us-west-1c'], 'ap-south-1':['ap-south-1a', 'ap-south-1b']}

# 3 Core Concepts
#
# 1. Launch Configuration
# 2. Autoscale Group
# 3. Triggers

for region in regions:
    autoscale_conn = boto.ec2.autoscale.connect_to_region(region)
    # First setup a Launch Configuration
    f = open('./files/userdata.txt')
    lc = LaunchConfiguration(name='pywebdev_launch_config3', image_id=amis[region],
                                 instance_type='t2.micro', # defaults to m1.small
                                 key_name='seth',
                                 user_data=f.read(), # Reads userdata.txt
                                 security_groups=['default'])
    result = autoscale_conn.create_launch_configuration(lc)
    print(region, ' Launch Configuration Creation Result: ', result)
    f.close()

    # Now we have a Launch Configuration and an ELB.  Create and launch the AutoScalingGroup
    ag = AutoScalingGroup(group_name='pywebdev_as_group2',
                              availability_zones=azs[region],
                              launch_config=lc, min_size=2, max_size=4,
                              connection=autoscale_conn)
    result = autoscale_conn.create_auto_scaling_group(ag)
    print(region, 'Auto Scaling Group Creation Result: ', result)
