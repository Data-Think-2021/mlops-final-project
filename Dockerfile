# Use a Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy the KMeans model script to the container
COPY kmeans_model.py /app/

# Create a data directory in the container
RUN mkdir /app/data

COPY data/bbc_news.csv.zip /app/data

# Install required Python packages
RUN pip install scikit-learn pandas prefect boto3 mlflow sentence_transformers 

# Set the command to run your batch processing script
CMD ["python", "kmeans_model.py", "data/bbc_news.csv.zip", "output_result.parquet"]
