{\rtf1\ansi\ansicpg1252\cocoartf2580
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import boto3\
\
bucket = 'zillow-data-input'\
prefix = 'Transformed_data/'\
\
s3 = boto3.client('s3')\
\
# List all objects under the prefix\
paginator = s3.get_paginator('list_objects_v2')\
for page in paginator.paginate(Bucket=bucket, Prefix=prefix):\
    if 'Contents' in page:\
        # Filter out the placeholder object (the "folder" itself)\
        objects_to_delete = [\
            \{'Key': obj['Key']\}\
            for obj in page['Contents']\
            if obj['Key'] != prefix  # This keeps the folder placeholder\
        ]\
        if objects_to_delete:\
            s3.delete_objects(Bucket=bucket, Delete=\{'Objects': objects_to_delete\})\
}