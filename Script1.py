
#Script checks and encrypts bucket that is not encrypted

import boto3
from botocore.exceptions import ClientError

s3Resource = boto3.resource('s3')
client = boto3.client('s3')
SSECNF = 'ServerSideEncryptionConfigurationNotFoundError'

response = client.list_buckets()

for bucket in response['Buckets']:
  try:
    enc = client.get_bucket_encryption(Bucket=bucket['Name'])
    rules = enc['ServerSideEncryptionConfiguration']['Rules']
    print(' Server Side Encryption enabled for bucket: %s, Encryption: %s' % (bucket['Name'], rules))
  except ClientError as e:
    if e.response['Error']['Code'] == SSECNF:
      print('Bucket: %s, no server-side encryption. Encrypting bucket now ' % (bucket['Name']))
      client.put_bucket_encryption(Bucket=bucket['Name'],
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
      print("Bucket: %s, unexpected error: %s" % (bucket['Name'], e))
