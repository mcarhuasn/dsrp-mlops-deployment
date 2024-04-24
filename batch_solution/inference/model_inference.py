"""
Este es un pipeline de inferencia (predicción) de un Modelo de Default Crediticio
"""

import mlflow
import pandas as pd
import dotenv
import os
from loguru import logger
import boto3
import pickle
import io

config = dotenv.dotenv_values(".env")
#print(config.get("MLFLOW_TRACKING_URI"))
#print(config.get("MLFLOW_TRACKING_USERNAME"))
#print(config.get("MLFLOW_TRACKING_PASSWORD"))

MLFLOW_TRACKING_URI = config.get("MLFLOW_TRACKING_URI")
AWS_ACCESS_KEY = config.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config.get("AWS_ACCESS_SECRET")

ID_VAR = "id"
TARGET_VAR = "loss"

MODEL_NAME = "default_prediction_dsrp_model"
CHAMPION_ALIAS = "dsrp-champion"
CHALLENGER_ALIAS = "dsrp-challenger"

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

def upload_csv_to_s3(dataframe: pd.DataFrame, bucket_name, path, aws_access_key_id=None, aws_secret_access_key=None):
    # Create a connection to S3
    if aws_access_key_id and aws_secret_access_key:
        s3 = boto3.client('s3', aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)
    else:
        s3 = boto3.client('s3')

    csv_buffer = io.StringIO()
    dataframe.to_csv("tmp.csv")

    s3.upload_file("tmp.csv", bucket_name, path)
    
def generate_predictions(model_alias: str, raw_data: pd.DataFrame, data: pd.DataFrame) -> None:
    logger.info(f"Downloading the {model_alias} model {MODEL_NAME}@{model_alias}")
    model = mlflow.sklearn.load_model(f"models:/{MODEL_NAME}@{model_alias}")
    
    logger.info(f"Predicting input data for the {model_alias} model... ")
    vector_predictions = model.predict(data)
    predictions = raw_data[[ID_VAR, TARGET_VAR]]
    predictions['loss_prediction'] = vector_predictions    
    
    print(predictions.head())
    
    logger.info(f"Uploading {model_alias} Predictions to S3 Bucket")
    upload_csv_to_s3(
                    dataframe = predictions,
                    bucket_name = config.get("S3_BUCKET_RAW_NAME"),
                    path = f"predictions/{model_alias}_predicciones_dsrp_mcn.csv",
                    aws_access_key_id = AWS_ACCESS_KEY,
                    aws_secret_access_key = AWS_SECRET_ACCESS_KEY
                    )    

logger.info("Reading data from S3")
raw_data = read_csv_from_s3(
                            bucket_name = config.get("S3_BUCKET_RAW_NAME"), 
                            file_key = "raw/sample_train_v2.csv",
                            aws_access_key_id = AWS_ACCESS_KEY,
                            aws_secret_access_key = AWS_SECRET_ACCESS_KEY
                            )

logger.info("Cleaning data input")
data = raw_data.replace("NA", 0)
data.drop([ID_VAR, TARGET_VAR], axis=1, inplace=True)
print(data.head())

li_models = [CHAMPION_ALIAS, CHALLENGER_ALIAS]

for model in li_models:
    generate_predictions(
                        model_alias=model,
                        raw_data=raw_data,
                        data=data
                        )
