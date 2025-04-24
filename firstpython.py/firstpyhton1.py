import boto3

ec2 = boto3.client('ec2')
response =ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
snapshots = ec2.describe_snapshots(OwnerIds=['self'])
instance_ids=set()
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_ids.add(instance['InstanceId'])
for snapshot in snapshots['Snapshots']:
    snapshotid =snapshot['SnapshotId']
    volume_id = snapshot['VolumeId']
    if not volume_id:
        ec2.delete_snapshot(SnapshotId=snapshotid)
        print(f"Deleted snapshot {snapshotid} for volume {volume_id}")
    else:   
        try:
            volume = ec2.describe_volumes(VolumeIds=[volume_id])
            if not volume['Volumes'][0]['Attachments']:
                ec2.delete_snapshot(SnapshotId=snapshotid)
        except ec2.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                # The volume associated with the snapshot is not found (it might have been deleted)
                ec2.delete_snapshot(SnapshotId=snapshotid)
                print(f"Deleted EBS snapshot {snapshotid} as its associated volume was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
   
