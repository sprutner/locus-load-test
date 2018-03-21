import boto3

regions = ['us-east-1', 'us-west-1', 'ap-south-1']
amis = {'us-east-1': 'ami-43a15f3e', 'us-west-1': 'ami-925144f2', 'ap-south-1': 'ami-0189d76e'}
azs = {'us-east-1': ['us-east-1a', 'us-east-1b', 'us-east-1c'], 'us-west-1': ['us-west-1b', 'us-west-1c'], 'ap-south-1':['ap-south-1a', 'ap-south-1b']}

# 3 Core Concepts
#
# 1. Launch Configuration
# 2. Autoscale Group
# 3. Triggers

for region in regions:
    autoscale_conn = boto3.client('autoscaling',region_name=region)
    # First setup a Launch Configuration
    f = open('./files/userdata.txt')
    lc = autoscale_conn.create_launch_configuration(LaunchConfigurationName='pywebdev_launch_config', ImageId=amis[region],
                                 InstanceType='t2.micro', # defaults to m1.small
                                 KeyName='seth',
                                 UserData=f.read(), # Reads userdata.txt
                                 SecurityGroups=['default'])

    print(region, ' Launch Configuration Creation Result: ', lc['ResponseMetadata']['HTTPStatusCode'])
    f.close()

    # Now we have a Launch Configuration and an ELB.  Create and launch the AutoScalingGroup
    ag = autoscale_conn.create_auto_scaling_group(AutoScalingGroupName='pywebdev_as_group',
                              AvailabilityZones=azs[region],
                              LaunchConfigurationName='pywebdev_launch_config', MinSize=1, MaxSize=1)
    print(region, 'Auto Scaling Group Creation Result: ', ag['ResponseMetadata']['HTTPStatusCode'])
