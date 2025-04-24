import boto3
iam = boto3.client('iam')
# List all IAM users
response = iam.list_users()
for user in response['Users']:
    print(user['UserName'])
    print(user['UserId'])
    print(user['Arn'])
    print(user['CreateDate'])
    print(user['PasswordLastUsed'])