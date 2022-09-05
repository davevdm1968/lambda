# Delete Volume Available older than
#
# @author Dave van der Merwe
#
# This script will search for all volumes that are in an available state 
# If the volume was detached more than older_than_days variable it will delete it
#
# The final delete step has been commented out so you can first test the script.
# Remove the # in front of #v.delete() for it to actually delete the volume.
#
import boto3
from datetime import datetime, timezone
#
older_than_days = 30 #
#
def detachdays(client, volume):
    try:
        response = client.lookup_events(
            LookupAttributes=[
                {
                    'AttributeKey': 'EventName',
                    'AttributeValue': 'DetachVolume'
                },
                {
                    'AttributeKey': 'ResourceName',
                    'AttributeValue': volume
                },
            ],
            #StartTime=datetime(2015, 1, 1),
            #EndTime=datetime(2015, 1, 1),
            #EventCategory='insight',
            MaxResults=1,
            #NextToken='string'
        )
        detachdate = response['Events'][0]['EventTime']
        print(f'{volume} detached {detachdate}')
        delta = datetime.now(timezone.utc) - detachdate
        return delta.days
    except:
        print(f'Unable to calculate detachdate for {volume}')
        return 0

def lambda_handler(object, context):

    # Get list of regions
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
               for region in ec2_client.describe_regions()['Regions']]

    for region in regions:
        ec2 = boto3.resource('ec2', region_name=region)
        client = boto3.client('cloudtrail', region_name=region)
        print("Region:", region)

        # List only unattached volumes ('available' vs. 'in-use')
        volumes = ec2.volumes.filter(
            Filters=[{'Name': 'status', 'Values': ['available']}])

        for volume in volumes:
            v = ec2.Volume(volume.id)
            if (detachdays(client, volume.id) > older_than_days):
                print("Deleting EBS volume: {}, Size: {} GiB".format(v.id, v.size))
                #v.delete()
#
