import boto3
client = boto3.client('s3')
from boto3.s3.transfer import TransferConfig


config = TransferConfig(use_threads=True,max_concurrency=500)
bucket='testttttttt8843543'

def iterate_bucket_items(bucket):
    """
    Generator that iterates over all objects in a given s3 bucket

    See http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.list_objects_v2
    for return data format
    :param bucket: name of s3 bucket
    :return: dict of metadata for an object
    """


    client = boto3.client('s3')
    paginator = client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket)

    for page in page_iterator:
        if page['KeyCount'] > 0:
            for item in page['Contents']:
                print(item)
                yield item



for i in iterate_bucket_items(bucket):
    date_add=str(i["LastModified"])
    src_key = i["Key"]
    src_bucket=bucket
    client.copy(Key=src_key, Bucket=src_bucket,Config=config,
        CopySource={"Bucket": src_bucket, "Key": src_key},
        ExtraArgs={
        "Metadata": {
            "creationDate": date_add
        },
        "MetadataDirective": "REPLACE",
        "ACL":'bucket-owner-full-control',
    }
        )
    print(i)
print("done")
