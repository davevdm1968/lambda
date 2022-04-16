# Automated instance termination
#
# @author Dave van der Merwe
#
# This script will search for all instances with out a tag key 'auto-delete' and
# will terminate it if it was created before today()
#
import boto3
import time

def lambda_handler(event, context):
    #
    today = time.strftime("%Y-%m-%d")
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    ec2c = boto3.client('ec2')
    regions = [region['RegionName']
            for region in ec2c.describe_regions()['Regions']]
    #
    for region in regions:
        print("Region:", region)
        ec2r = boto3.resource('ec2', region_name=region)
        #reservations = ec2.describe_instances(Filters=[{
        #    "Name": "instance-state-name",
        #    "Values": ["stopped"],
        #}]).get("Reservations")

        #instances = [r.get("Instances") for r in reservations]
        instances = ec2r.instances.all()
        #print("Found %d instances that need evaluated" % len(instances))
        for instance in instances:
            if instance.tags is not None and 'auto-delete' not in [t['Key'] for t in instance.tags]:
                print("Checking ", instance.id)
                launchdate = instance.launch_time.strftime("%Y-%m-%d")
                if launchdate != today:
                    print("Terminating instance ", instance.id)
                    print(instance.terminate())
            else:
                print("Skipping ", instance.id)
#
