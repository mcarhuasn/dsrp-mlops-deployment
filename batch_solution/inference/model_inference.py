import mlflow
import pandas as pd
import dotenv
import os
from loguru import logger
import boto3
import pickle
import io

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

def upload_csv_to_s3(dataframe: pd.DataFrame, bucket_name, path, aws_access_key_id=None, aws_secret_access_key=None):
    # Create a connection to S3
    if aws_access_key_id and aws_secret_access_key:
        s3 = boto3.client('s3', aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)
    else:
        s3 = boto3.client('s3')

    csv_buffer = io.StringIO()
    #dataframe.to_csv(csv_buffer)
    dataframe.to_csv("tmp.csv")

    #s3.Object(bucket_name, path).put(Body=csv_buffer.getvalue())
    #s3.upload_file(csv_buffer.getvalue(), bucket_name, path)
    s3.upload_file("tmp.csv", bucket_name, path)
    

logger.info("Reading data from S3")
AWS_ACCESS_KEY = config.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config.get("AWS_ACCESS_SECRET")
ID_VAR = "id"
TARGET_VAR = "loss"

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

#default_model = mlflow.sklearn.load_model(model_uri=f"models:/default_prediction_dsrp_model/Production",)
#default_model = mlflow.sklearn.load_model(model_uri=f"models:/default_prediction_dsrp_model/versions/1",)
#default_model = mlflow.sklearn.load_model(model_uri=f"runs:/c5d12be616c54ae3b30e2b301a82a50f/default_prediction_dsrp_model",)
#print(default_model)
mlflow.set_registry_uri(config.get("MLFLOW_TRACKING_URI"))
model_name = "default_prediction_dsrp_model"
alias = "dsrp-champion"

logger.info(f"Downloading the Champion model {model_name}@{alias}") 
#model_path = mlflow.artifacts.download_artifacts("mlflow-artifacts:/c5d12be616c54ae3b30e2b301a82a50f/95ec71c8d38c47a29d71f3be11a8a7ab/artifacts/model/model.pkl") # XGBoost pkl model file
#with open(model_path, "rb") as file:
#    model = pickle.load(file)
#
champion_model = mlflow.sklearn.load_model(f"models:/{model_name}@{alias}")

logger.info("Predicting input data for Champion model... ")
champion_vector_predictions = champion_model.predict(data)
champion_predictions = raw_data[[ID_VAR, TARGET_VAR]]
champion_predictions['loss_prediction'] = champion_vector_predictions
print(champion_predictions.head())

logger.info(f"Downloading the Challenger model {model_name}")
challenger_model = mlflow.sklearn.load_model(f"models:/{model_name}@dsrp-challenger") 

logger.info("Predicting input data for Challenger model... ")
challenger_vector_predictions = challenger_model.predict(data)
challenger_predictions = raw_data[[ID_VAR, TARGET_VAR]]
challenger_predictions['loss_prediction'] = challenger_vector_predictions
print(challenger_predictions.head())


logger.info("Uploading Predictions to S3 Bucket")
upload_csv_to_s3(
                dataframe = champion_predictions,
                bucket_name = config.get("S3_BUCKET_RAW_NAME"),
                path = "predictions/champion_predicciones_dsrp_mcn.csv",
                aws_access_key_id = AWS_ACCESS_KEY,
                aws_secret_access_key = AWS_SECRET_ACCESS_KEY
                )

upload_csv_to_s3(
                dataframe = challenger_predictions,
                bucket_name = config.get("S3_BUCKET_RAW_NAME"),
                path = "predictions/challenger_predicciones_dsrp_mcn.csv",
                aws_access_key_id = AWS_ACCESS_KEY,
                aws_secret_access_key = AWS_SECRET_ACCESS_KEY
                )

