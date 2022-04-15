# Snapshot Deletion
#
# @author Dave van der Merwe
#
# This script will search for all snapshots that were created by AMIs were the
# AMI does not exist any longer and delete the snapshot

import boto3
import time
import sys

def lambda_handler(event, context):
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    ec2 = boto3.client('ec2')
    regions = [region['RegionName']
               for region in ec2.describe_regions()['Regions']]

    for region in regions:
        print("Region:", region)
        ec2 = boto3.client('ec2', region_name=region)
        response = ec2.describe_snapshots(OwnerIds=[account_id])
        snapshots = response["Snapshots"]

        for snapshot in snapshots:
            #print(snapshot)
            if snapshot['Description'].find("Created by CreateImage") == 0:
                #print(snapshot)
                print("Checking ", snapshot['SnapshotId'])
                amiid = "ami-" + snapshot['Description'].partition("for ami-")[2]
                print("Checking ",amiid)
                try:
                    response = ec2.describe_image_attribute(
                        Attribute='description',
                        ImageId=amiid
                    )
                    print("Found    ", amiid)
                except:
                    print("AMI NOT found ", amiid)
                    if snapshot['Description'].find(amiid) > 0:
                        snap = ec2.delete_snapshot(
                            SnapshotId=snapshot['SnapshotId'])
                    print("Deleting snapshot " + snapshot['SnapshotId'])
#
