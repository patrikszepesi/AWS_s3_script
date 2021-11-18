# import boto3
# s3 = boto3.resource('s3')
# s3client = boto3.client('s3')
#
#
# for bucket in s3.buckets.all():
#     for key in bucket.objects.all():
#         print(key.key)
#     print("New Bucket")

# import boto3
# s3 = boto3.resource('s3')
# s3client = boto3.client('s3')
#
#
# for bucket in s3.buckets.all():
#     for key in bucket.objects.all():
#         date_add=str(key.last_modified)
#         print(date_add)
#         #print(key.last_modified)
#         key.put(Metadata={'CreateDate':date_add})
#         #object_summary = s3.ObjectSummary(bucket,key)
#         #print(object_summary)
#     print("New Bucket")
#


# import boto3
# s3 = boto3.resource('s3')
# s3client = boto3.client('s3')
#
#
# for bucket in s3.buckets.all():
#     for key in bucket.objects.all():
#         date_add=str(key.last_modified)
#         s3_object = s3.Object(bucket, key)
#         print(bucket)
#         s3_object.metadata.update({'x-amz-meta-date':date_add})
#         s3_object.copy_from(CopySource={'Bucket':bucket, 'Key':key}, Metadata=s3_object.metadata, MetadataDirective='REPLACE')
#
#     print("New Bucket")


import boto3
s3 = boto3.resource('s3')
s3client = boto3.client('s3')
s3Client = boto3.client("s3")



for bucket in s3.buckets.all():
    for key in bucket.objects.all():
        date_add=str(key.last_modified)
        src_key = key.key
        src_bucket=bucket.name
        s3Client.copy_object(Key=src_key, Bucket=src_bucket,
                       CopySource={"Bucket": src_bucket, "Key": src_key},
                       Metadata={"creationDate": date_add},
                       MetadataDirective="REPLACE")

    print("New Bucket")
