## 1. Background

People are excited of LLM and GenAI. I worked recently a lot on text data. Unfortunately, the ChatGPT model can't cluster the text data. However, we can use the pre-trained language model to do the embeddings to capture their semantic meaning. Then with unsupervised learning models like Kmeans I build this end-to-end ML project as final project of this Zoomcamp. 


## 2. Data
* Dataset was downloaded from [BBC-News Data on Kaggle](https://www.kaggle.com/datasets/gpreda/bbc-news). 

## 3. Overview and Architecture
The MLops project consists 6 main components: ML modeling, Experiments tracking, Workflow orchetration, Batch Deployment, Monitoring, and Managing cloud resource with Terraform. Due to the limited time, I was not able to implement all of them. 
![flowchart](https://res.cloudinary.com/do5aglxsw/image/upload/v1690832009/mlops-final-project-bbc-clustering/flowchart_mlops.drawio_tzkwxs.png)


## 4. Technologies 

* Cloud: AWS
* Experiment tracking tools: MLFlow
* Workflow orchestration: Prefect  
~~* Monitoring: Evidently~~  
~~* CI/CD: Github actions~~  
~~* Infrastructure as code (IaC): Terraform~~  

## 5. Steps to reproduce
### 5.1 Setup environment 
* Create a virtual environment

* Install libraries
```shell
pipenv install mlflow scikit-learn prefect pandas boto3 sentence-transformers seaborn
```

* Activate the virtual environment, run ```pipenv shell```

* Show the path of  the virtual env, run ```pipenv --venv```  
/Users/xiahe/.local/share/virtualenvs/mlops-final-project-70huLeJa 

* Set the python interpreter in VS code. ctrl+shift+p -> choose python interpreter -> add the python above /Users/xiahe/.local/share/virtualenvs/mlops-final-project-70huLeJa/**bin/python**


### 5.2 AWS 
Set the environment variables for AWS configuration.
```shell
export AWS_ACCESS_KEY_ID=[AWS_ACCESS_KEY_ID]
export AWS_SECRET_ACCESS_KEY=[AWS_SECRET_ACCESS_KEY]
```

First create a permission policy so that Boto3 can write and list S3 Bucket.
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::mlflow-remote/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::mlflow-remote"
            ]
        }
    ]
}
```

### 5.3 Clustering Steps
1. Read data
2. Do embedding
3. Prepare input matrix for KMeans model
4. Clustering with Kmeans

### 5.4 Experiment monitoring with MLflow with remote host server on AWS
MLflow setup:
* Tracking server: yes, remote server (EC2).
* Backend store: postgresql database.
* Artifacts store: s3 bucket.

1. Lauch an instance EC2. Edit inbound rules, allowing Http Custom TCP on Port 5000 from all IP trafic.
2. Create a S3 bucket in eu-central-1.
3. Create AWS RDS, choose PostgreSQL as engine type. Select security group of the database. Edit inbound rules, allow EC2 Instance to connect to DB.Choose postgreSQL type, Chooose the security group which was created by launching EC2. 
4. Connect to EC2 and run the following command in EC2 to start mlflow server. 
```shell
mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri postgresql://mlflow:mlflowadmin@...../mlflow_db --default-artifact-root s3://mflow-remote
```
Go to EC2 and copy the public ID. open EC2-public-IP:5000 to see all your experiments. 
If you are satisfied with one model, you can register model. 

* Train a model on that dataset tracking your experiments


Artifacts  
![mlflow artifact](https://res.cloudinary.com/do5aglxsw/image/upload/v1690834278/mlops-final-project-bbc-clustering/1_ztivqa.png)



5. Create a model training pipeline
```pipenv install --dev jupyter_contrib_nbextensions```  
To turn the notebook into a script, use```jupyter nbconvert --to script bbc_news_clustering.ipynb```. 
Convert the code into different tasks using prefect to orchestrate the whole pipeline.
Run python code ```python clustering_remote.py```. 

Registered Model  
![mlflow artifact](https://res.cloudinary.com/do5aglxsw/image/upload/v1690834278/mlops-final-project-bbc-clustering/2_nvjzzr.png)



### 5.5 Use Prefect to do orchestration
Start the Prefect server using ```prefect server start```. Check out the dashboard at http://127.0.0.1:4200. 
```pipenv install prefect_aws```  Create and save artifacts to s3 bucket. 

Run the python code and the artifacts are saved in s3 buckets.
default artifacts URI: 's3://mflow-remote/1/95ff04c0e1a64edea415d5749d473e6f/artifacts'

![Flow](https://res.cloudinary.com/do5aglxsw/image/upload/v1690834278/mlops-final-project-bbc-clustering/3_ekn6jo.png)


### 5.6 Deploy the model in batch
Batch deployment. Fetch the model from s3 artifact. Feed the new data to the model and assign them the clusters. 
```python kmeans_model.py data/bbc_news.csv.zip data/output_cluster.parquet```


Build the docker image:

```shell
docker build -t mlops-zoomcamp-bbc-news-clustering:v1 .
```

Run the docker image on local env
```shell
docker run -it --rm -e AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" -e AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" --name mlops-project mlops-zoomcamp-bbc-news-clustering:v1
```


### 5.7 Best practice
* Unit tests
    ```pipenv install --dev pytest```
* Code quality check
Intall pylint with ```pipenv install --dev pylint```. Then ```pylint --recursive=y .```. You will a lot of comments and rate score from pylint.

To view it from VS code, press ctrl+shift+p, search Python:Select Linter. 

* Makefile
    makefile is already installed in linux machine.
    use ```make test```




