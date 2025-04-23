import boto3
ec2 = boto3.client('ec2')
response = ec2.describe_instances(filters=[{"Name": "instance-state-name", "Values": ["running"]}])
snapshots = ec2.describe_snapshots(OwnerIds=['self'])
instances_ids = set()

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instances_ids.add(instance['InstanceId'])
for snapshots in snapshots['Snapshots']:
   snapshotid = snapshots['SnapshotId']
   voulmeid = snapshots['VolumeId']
   if not voulmeid:
       ec2.delete_snapshot(SnapshotId=snapshotid)
       print(f"Deleted snapshot {snapshotid} with volume ID {voulmeid}")
   else:
        try:
            volume = ec2.describe_volumes(VolumeIds=[voulmeid])
            if not volume['Volumes'][0]['Attachments']:
                ec2.delete_snapshot(SnapshotId=snapshotid)
                print(f"Deleted snapshot {snapshotid} with volume ID {voulmeid}")      
        except Exception.clienterror as e:
            if e.response['Error']['Code'] == 'Invalidvolume.NotFound':
                print(f"Snapshot {snapshotid} is in use and cannot be deleted.")
                ec2.delete_snapshot(SnapshotId=snapshotid)
           