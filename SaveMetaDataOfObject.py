import boto3
import time
from botocore.exceptions import ClientError
from botocore.config import Config


bucket='test-101-test'

config = Config(
   retries = {
      'max_attempts': 10,
      'mode': 'standard'
   }
)

client = boto3.client('s3',config=config)

def iterate_bucket_items(bucket):
    try:
        paginator = client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket)
        for page in page_iterator:
            if page['KeyCount'] > 0:
                for item in page['Contents']:
                    print(item)
                    yield item

    except ClientError as exception_obj:
        if exception_obj.response['Error']['Code'] == 'ThrottlingException':
            print("ThrottlingException caught")
            time.sleep(0.3)
            return iterate_bucket_items(bucket)
        else:
            print(f"unexpected error {exception_obj}")

for i in iterate_bucket_items(bucket):
    date_add=str(i["LastModified"])
    src_key = i["Key"]
    src_bucket=bucket
    try:
        client.copy_object(Key=src_key, Bucket=src_bucket,
            ACL='bucket-owner-full-control',
            CopySource={"Bucket": src_bucket, "Key": src_key},
            Metadata={"creationDate": date_add},
            MetadataDirective="REPLACE")
            #print(i)
    except ClientError as exception_obj:
        if exception_obj.response['Error']['Code'] == 'ThrottlingException':
            print("ThrottlingException caught")
            time.sleep(0.3)
        else:
            print(f"unexpected error {exception_obj}")
