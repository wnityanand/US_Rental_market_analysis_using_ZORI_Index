import sys
import boto3
import os
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from awsglue.job import Job

# Define the move_s3_file function to move files
def move_s3_file(s3_client, source_bucket, source_key, dest_bucket, dest_prefix):
    """
    Moves a file from one S3 location to another.

    Args:
        s3_client: Boto3 S3 client.
        source_bucket: Source S3 bucket name.
        source_key: Source S3 key (file path).
        dest_bucket: Destination S3 bucket name.
        dest_prefix: Destination S3 prefix (folder).
    """
    dest_key = os.path.join(dest_prefix, os.path.basename(source_key))
    copy_source = {'Bucket': source_bucket, 'Key': source_key}
    try:
        s3_client.copy(copy_source, dest_bucket, dest_key)
        s3_client.delete_object(Bucket=source_bucket, Key=source_key)
        print(f"Moved {source_key} to s3://{dest_bucket}/{dest_key}")
    except Exception as e:
        print(f"Error moving {source_key}: {e}")

# Glue job setup
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Hardcoded S3 locations
source_bucket = "zillow-data-input"  # Replace with your source bucket
source_prefix = "unprocess-file/"  # Replace with your source folder
dest_bucket = "zillow-data-input"  # Replace with your destination bucket
dest_prefix = "process-file/"  # Replace with your destination folder

# Initialize S3 client
s3_client = boto3.client('s3')

# List files in the source S3 location
try:
    response = s3_client.list_objects_v2(Bucket=source_bucket, Prefix=source_prefix)
    files = response.get('Contents', [])
except Exception as e:
    print(f"Error listing objects in S3: {e}")
    sys.exit(1)

# Move each file to the destination location
for file in files:
    source_key = file['Key']
    if source_key.startswith(source_prefix) and source_key.endswith('.csv'):  # Process CSV files in source folder
        move_s3_file(s3_client, source_bucket, source_key, dest_bucket, dest_prefix)

job.commit()

