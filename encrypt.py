
#ENCRYPT BUCKET IF NOT ENCRYPTED ALREADY
import boto3
from botocore.exceptions import ClientError


s3 = boto3.client('s3')

response = s3.list_buckets()
client = boto3.client('s3')
SSECNF = 'ServerSideEncryptionConfigurationNotFoundError'
for bucket in response['Buckets']:
  try:
    bucket = client.get_bucket_encryption(Bucket=bucket['Name'])
    # check current encryption here, if it's not what you want then update it
    # check bucket['ServerSideEncryptionConfiguration']['Rules']
  except client.exceptions.ClientError as e:
    if e.response['Error']['Code'] == SSECNF:
        s3.put_bucket_encryption(Bucket=bucket['Name'],
        ServerSideEncryptionConfiguration={
          'Rules': [
            {
                'ApplyServerSideEncryptionByDefault': {
                    'SSEAlgorithm': 'AES256'
                }
            },
          ]
        })
    else:
        print("Unexpected error: %s" % e)
