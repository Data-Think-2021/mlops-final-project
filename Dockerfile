# Use a Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy the KMeans model script and data to the container
COPY kmeans_model.py /app/
COPY data/bbc_news.csv.zip /app/

# Install required Python packages
RUN pip install scikit-learn pandas

# Set the command to run your batch processing script
CMD ["python", "kmeans_model.py", "bbc_news.csv.zip"]
