"""
 DAG para ejecutar predicciones desde un modelo registrado en MLFlow
"""
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd


print("Hello Airflow!!!")
