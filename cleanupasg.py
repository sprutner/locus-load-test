import boto.ec2.autoscale
import time

regions = ['us-east-1', 'us-west-1', 'ap-south-1']
# regions = ['us-west-1']

for region in regions:
    autoscale_conn = boto.ec2.autoscale.connect_to_region(region)

    try:
        ag = autoscale_conn.get_all_groups(names=['pywebdev_as_group'])[0]
    except IndexError:
        print(region, " No ASG to cleanup")
        continue

    print(region, " PyWebDev AS Group: ", ag)

    # Once the instances have been shutdown, you can delete the autoscale group:
    print('Shutting down instances for ag: ', ag)
    ag.shutdown_instances()
    time.sleep(60)
    print('Deleting ASG', ag)
    try:
        ag.delete()
    except:
        print("Scaling activity already in process, retrying")
        retries = 3
        for i in range(retries):
            try:
                time.sleep(30)
                ag.delete()
            except:
                if i < retries - 1:
                    continue
                else:
                    raise
            break

        else:
            print("Unexpected error: {}".format(e))
    time.sleep(20)

# Delete LCs
for region in regions:
    autoscale_conn = boto.ec2.autoscale.connect_to_region(region)

    # Now get the Launch Configuration
    lc = autoscale_conn.get_all_launch_configurations(names=['pywebdev_launch_config'])[0]
    print(region, " PyWebDev LC: ", lc)

    lc.delete()

# Delete SQS queues
for region in regions:
    sqs = boto3.client('sqs', region_name=region)
    try:
        queue = sqs.delete_queue(QueueName=Q)
        print('{} Queue: {} Deleted'.format(region, Q))
    except ClientError as e:
        print ("Queue does not exist", e)
