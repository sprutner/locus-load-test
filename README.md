## Multi - Region Locust Load Tester ##

This app start a flask web-app that runs locally, and then creates a load-test using Locust on targeted websites.

The script uses boto3 to create AutoScalingGroups in selected regions that are bootstrapped with locust. The webapp will pass your inputs into an SQS message that will be read by the workers and then will run a locust load-test with the properties specified in the web app. Once complete, a CSV will be uploaded to your S3 bucket.

### Execution ###

```python app.py```
And then navigate to http://localhost:5000 in a browser

run `python cleanup.py` when finished to delete resources

### Pre-requisties ###

-need to create key_pair per region
-specify a bucket name and then hardcode it in files/userdata.txt
-iam instance profile with s3 and sqs permission for as
-AWS credentials must be set locally with with .credentials file or environment variables:
e.g.

```
AWS_ACCESS_KEY_ID=access-key
AWS_SECRET_ACCESS_KEY=securepassword```

### Issues / To Do ###
- Hardcoded S3 bucket URI in user-data script.
-- Terraform templating would solve this Issues
- Boot time can be faster
-- Packerifying AMIs would be ideal.
- Autoscaling policies not yet created
-- Need to determine best thresholds. CPU usage for this application may not be appropriate, logic on the amount of users and the instance size is probably a better indication of resource needs and triggering a scaling action
- Distributed mode not being utilized
-- With autoscaling implementation, logic can be added to the SQS message to tell locust to enter distributed mode and wait for x server to come up before it runs its requests
- Boto3 not fully being used in cleanup script
- Speed up cleanup
