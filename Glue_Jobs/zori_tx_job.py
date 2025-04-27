import sys
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as f
from pyspark.sql.types import *
import boto3

## @params: JOB_NAME
args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Set your bucket and desired subfolder path
bucket_name = "zillow-data-input"
subfolder_path = "Transformed_data/"

# Create a zero-byte object to represent the subfolder
s3 = boto3.client("s3")
s3.put_object(Bucket=bucket_name, Key=subfolder_path)

# Define input and output paths
s3_input = "s3://zillow-data-input/unprocess-file/Metro_zori_uc_sfrcondomfr_sm_month_april_16_2025.csv"
s3_target = "s3://zillow-data-input/Transformed_data/"

# Read the CSV file directly from S3 (infer schema)
df = spark.read.csv(s3_input, header=True, inferSchema=True)

# Identify columns to unpivot (date columns)
id_vars = ["RegionID", "SizeRank", "RegionName", "RegionType", "StateName"]
date_columns = [col for col in df.columns if col not in id_vars]

# Unpivot the data (melt)
df_melted = df.select(
    id_vars
    + [
        f.expr(
            "stack({}, {})".format(
                len(date_columns),
                ", ".join("'{}', `{}`".format(c, c) for c in date_columns),
            )
        ).alias("Date", "ZORI")
    ]
)

# Convert Date to date type
df_melted = df_melted.withColumn("Date", f.to_date(df_melted["Date"], "yyyy-MM-dd"))

# Write to S3 as Parquet
df_melted.write.mode("overwrite").partitionBy("RegionType", "StateName").parquet(
    s3_target
)

job.commit()
