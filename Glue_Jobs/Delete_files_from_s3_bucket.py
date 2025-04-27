import boto3

bucket = "zillow-data-input"
prefix = "Transformed_data/"

s3 = boto3.client("s3")

# List all objects under the prefix
paginator = s3.get_paginator("list_objects_v2")
for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
    if "Contents" in page:
        # Filter out the placeholder object (the "folder" itself)
        objects_to_delete = [
            {"Key": obj["Key"]}
            for obj in page["Contents"]
            if obj["Key"] != prefix  # This keeps the folder placeholder
        ]
        if objects_to_delete:
            s3.delete_objects(Bucket=bucket, Delete={"Objects": objects_to_delete})