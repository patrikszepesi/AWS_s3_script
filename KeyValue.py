import boto3


s3 = boto3.client('s3')

response = s3.list_buckets()
client = boto3.client('s3')
SSECNF = 'ServerSideEncryptionConfigurationNotFoundError'
for bucket in response['Buckets']:
    for key, value in bucket.items():
        print(key,":",value)
