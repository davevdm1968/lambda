# Stop Instance
#
# @author Dave van der Merwe
#
# This script will search for all instances with tag auto-stop with value yes and stop the instance
# 
import boto3
#
#filters = [{"Name":"tag:auto-stop","Values":["yes"]},{"Name":"tag:awssupport:patchwork","Values":["patch"]}]
filters = [{"Name":"tag:auto-stop","Values":["yes"]}]
#
def lambda_handler(event, context):
    # List all regions
    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    for region in regions:
        session = boto3.Session(region_name=region)
        ec2resource = session.resource('ec2')
        instances = ec2resource.instances.filter(Filters=filters)
        for instance in instances:
            print(f'Stopping instance {instance.instance_id}')
            instance.stop()
    #
#
