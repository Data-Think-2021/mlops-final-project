import pandas as pd
import numpy as np
import mlflow
from prefect import task, flow
from prefect_aws.s3 import S3Bucket

from sentence_transformers import SentenceTransformer

from sklearn.cluster import KMeans


@task(name='read_data', retries=3, retry_delay_seconds=2)
def read_data(filename:str)->pd.DataFrame:  
    df = pd.read_csv(filename, compression='zip')
    df['news'] = df['title'] + ' ' + df['description']

    return df 

@task(name='embedding_text', retries=3, retry_delay_seconds=2)
def prepare_embedding(df):
    # Sentence Transformers pip install -U sentence-transformers
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    df['news_embedding'] = model.encode(df['news'], convert_to_tensor=True).tolist()
    return df 


@task(name='prepare_input_matrix', retries=3, retry_delay_seconds=2)
def cal_input_matrix(df):
    embdding = df.loc[:, 'news_embedding'].apply(np.array) # .apply(eval).Convert string to numpy array
    matrix = np.vstack(embdding.values)
    return matrix


@task(name='clustering', retries=3, retry_delay_seconds=2)
def clustering(matrix):
    with mlflow.start_run():
        # Train KMeans model 
        params = {'n_clusters': 20,  'init': 'k-means++', 'random_state': 42}
        mlflow.log_params(params)

        kmeans = KMeans(**params)
        kmeans.fit(matrix)
        # labels = kmeans.labels_

        mlflow.sklearn.log_model(kmeans, artifact_path='models')
        print(f"default artifacts URI: '{mlflow.get_artifact_uri()}'")

    
@flow
def main_flow():
    # MLflow settings
    TRACKING_SERVER_HOST = "ec2-18-195-159-235.eu-central-1.compute.amazonaws.com"
    mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:5000")
    
    mlflow.set_experiment("kmeans-clustering-experiment")
    
    # Load the data
    s3_bucket_block = S3Bucket.load("my")
    s3_bucket_block.download_folder_to_path(from_folder="data", to_folder="data")
   
    df = read_data("data/bbc_news.csv.zip")
    df = prepare_embedding(df)

    # Transform
    matrix = cal_input_matrix(df)
  
    # Train
    clustering(matrix)


if __name__ == '__main__':
    main_flow()