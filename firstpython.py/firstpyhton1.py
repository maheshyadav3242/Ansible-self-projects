import boto3
ec2 = boto3.client('ec2')
response = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
snapshoots_response = ec2.describe_snapshots(OwnerIds=['self'])

active_instances_ids = set()

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
      
        active_instances_ids.add(instance['InstanceId'])
for snapshot in snapshoots_response['Snapshots']:
    snapshot_id = snapshot['SnapshotId']
    volume_id = snapshot.get('VolumeId')
    print("no snapshot id")
    if not volume_id:
        ec2.delete_snapshot(SnapshotId=snapshot_id)
    else:
        volume_response = ec2.describe_volumes(VolumeIds=[volume_id])
        if not volume_response['Volumes'][0]['Attachments']:
            print(f"Deleting snapshot {snapshot_id} for volume {volume_id}")
            ec2.delete_snapshot(SnapshotId=snapshot_id)