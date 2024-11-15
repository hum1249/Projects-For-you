import boto3
import pandas as pd
import os

from dotenv import load_dotenv
load_dotenv()

s3_client=boto3.client("s3",aws_access_key_id=os.getenv('aws_access_key_id'),aws_secret_access_key=os.getenv("aws_secret_access_key"))

