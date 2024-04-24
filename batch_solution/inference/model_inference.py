import mlflow
import pandas as pd
import dotenv
import os
from loguru import logger
import boto3

config = dotenv.dotenv_values(".env")
print(config.get("MLFLOW_TRACKING_URI"))
print(config.get("MLFLOW_TRACKING_USERNAME"))
print(config.get("MLFLOW_TRACKING_PASSWORD"))

MLFLOW_TRACKING_URI = config.get("MLFLOW_TRACKING_URI")

logger.info(f"El servidor de MLFlow es {MLFLOW_TRACKING_URI}")

os.environ["MLFLOW_TRACKING_USERNAME"] = config.get("MLFLOW_TRACKING_USERNAME")
os.environ["MLFLOW_TRACKING_PASSWORD"] = config.get("MLFLOW_TRACKING_PASSWORD")

#print(os.getcwd())

mlflow.set_tracking_uri(uri=MLFLOW_TRACKING_URI,)

def read_csv_from_s3(bucket_name, file_key, aws_access_key_id=None, aws_secret_access_key=None):
    # Create a connection to S3
    if aws_access_key_id and aws_secret_access_key:
        s3 = boto3.client('s3', aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)
    else:
        s3 = boto3.client('s3')

    # Read the CSV file
    obj = s3.get_object(Bucket = bucket_name, Key = file_key)
    df = pd.read_csv(obj['Body'])

    return df

logger.info("Reading data from S3")
AWS_ACCESS_KEY = config.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config.get("AWS_ACCESS_SECRET")
ID_VAR = "id"
TARGET_VAR = "loss"

data = read_csv_from_s3(
                        bucket_name = config.get("S3_BUCKET_RAW_NAME"), 
                        file_key = "raw/sample_train_v2.csv",
                        aws_access_key_id = AWS_ACCESS_KEY,
                        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
                        )

logger.info("Cleaning data input")
data.replace("NA", 0, inplace=True)
data.drop([ID_VAR, TARGET_VAR], axis=1)
print(data.head())

#default_model = mlflow.sklearn.load_model(model_uri=f"models:/default_prediction_dsrp_model/Production",)
#default_model = mlflow.sklearn.load_model(model_uri=f"models:/default_prediction_dsrp_model/versions/1",)
#print(default_model)
