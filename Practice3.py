import boto3
client = boto3.client('s3')
from boto3.s3.transfer import TransferConfig
#4:03 5.5 million threshol io chunksize 2621440
#3:59 5.5 million threshol io chunksize 262144
#3:55 5.5 131144

#https://stackoverflow.com/questions/46556972/what-is-optimal-setting-for-multipart-threshold-and-mutilpart-chunksize-while-do
#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.TransferConfig
#multipart chuncisze 100mb, multipiart 5 gb,download attempts 100, max io chunck size 10mb,
config = TransferConfig(use_threads=True,max_concurrency=100,multipart_chunksize=100886080,num_download_attempts=100,multipart_threshold=5500000,io_chunksize=10262144)
bucket='foo-bucket83485345'

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
