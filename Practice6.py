#Script saves metadata

#which bucket csv
#paginator
#try catch

import boto3
from botocore.exceptions import ClientError

s3Resource = boto3.resource('s3')
client = boto3.client('s3')


for bucket in s3Resource.buckets.all():
    #TRY BLOCK?
    for key in bucket.objects.all():
        print(key)
        date_add=str(key.last_modified)
        src_key = key.key
        src_bucket=bucket.name
        client.copy_object(Key=src_key, Bucket=src_bucket,
                       CopySource={"Bucket": src_bucket, "Key": src_key},
                       Metadata={"creationDate": date_add},
                       MetadataDirective="REPLACE")

    print("Saving next Bucket")
