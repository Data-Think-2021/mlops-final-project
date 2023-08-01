# Use a Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock /app/

# Install pipenv
RUN pip install pipenv

# Install required Python packages using pipenv
RUN pipenv install --system --deploy

# Copy the KMeans model script to the container
COPY kmeans_model.py /app/

# Create a data directory in the container
RUN mkdir /app/data

COPY data/bbc_news.csv.zip /app/data

# Set the command to run your batch processing script
CMD ["python", "kmeans_model.py", "data/bbc_news.csv.zip", "output_result.parquet"]
