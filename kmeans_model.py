#!/usr/bin/env python
# Batch production

import os
import sys

from datetime import datetime

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import mlflow

from prefect import task, flow, get_run_logger
from prefect.context import get_run_context


def read_dataframe(filename: str):
    df = pd.read_csv(filename, compression='zip')
    df['news'] = df['title'] + ' ' + df['description']

    return df.head()

def prepare_embedding(df: pd.DataFrame):
    # Sentence Transformers pip install -U sentence-transformers
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    df['news_embedding'] = model.encode(df['news'], convert_to_tensor=True).tolist()
    return df     

def cal_input_matrix(df):
    embdding = df.loc[:, 'news_embedding'].apply(np.array) # .apply(eval).Convert string to numpy array
    matrix = np.vstack(embdding.values)
    return matrix

def load_model():
    logged_model = f's3://mflow-remote/artifacts/models/'
    model = mlflow.pyfunc.load_model(logged_model)
    return model

def save_results(df, y_pred, output_file):
    df_result = pd.DataFrame()
    df_result['kmeans_cluster'] = y_pred
    df_result['model_version'] = 'v1'

    df_result.to_parquet(output_file, index=False)

@task
def apply_model(input_file, output_file):
    logger = get_run_logger()

    logger.info(f'reading the data from {input_file}...')
    df = read_dataframe(input_file)
    df = prepare_embedding(df)
    matrix = cal_input_matrix(df)

    logger.info(f'loading the model ...')
    model = load_model()

    logger.info(f'applying the model...')
    y_pred = model.predict(matrix)

    logger.info(f'saving the result to {output_file}...')

    save_results(df, y_pred, output_file)
    return output_file

@flow
def run():
    input_file = sys.argv[1] # 'data/bbc_news.csv.zip'
    output_file = sys.argv[2]  # 'data/output_cluster.parquet'
    
    apply_model(input_file, output_file)

if __name__ == '__main__':
    run()