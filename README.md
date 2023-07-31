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
~~* Monitoring: Evidently ~~  
~~* CI/CD: Github actions~~  
~~* Infrastructure as code (IaC): Terraform~~  

## 5. Steps to reproduce
### 5.1 Setup environment 
* Create a virtual environment

* Install libraries
```shell
pipenv install mlflow scikit-learn prefect pandas boto3 sentence-transformers seaborn
```

* Activate the virtual environment, run ```shellpipenv shell```

* Show the path of  the virtual env, run ```pipenv --venv```
/Users/xiahe/.local/share/virtualenvs/mlops-final-project-70huLeJa 

* Set the python interpreter in VS code. ctrl+shift+p -> choose python interpreter -> add the python above /Users/xiahe/.local/share/virtualenvs/mlops-final-project-70huLeJa/**bin/python**


### 5.2 AWS 

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
AWS EC2 as tracking server host, save artifacts to AWS S3. 
* Train a model on that dataset tracking your experiments
use ```mlflow ui```, open http://127.0.0.1:5000 to see all your experiments. 
If you are satisfied with one model, you can register model. 

![mlflow artifact](https://res.cloudinary.com/do5aglxsw/image/upload/v1690834278/mlops-final-project-bbc-clustering/1_ztivqa.png)

* Create a model training pipeline
```pipenv install --dev jupyter_contrib_nbextensions```  
To turn the notebook into a script, use```jupyter nbconvert --to script bbc_news_clustering.ipynb```. 
Convert the code into different tasks using prefect to orchestrate the whole pipeline.

```shell
mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri postgresql://mlflow:mlflowadmin@mlflow-database.cmzjefzzw99w.eu-central-1.rds.amazonaws.com:5432/mlflow_db --default-artifact-root s3://mflow-remote
```

![mlflow artifact](https://res.cloudinary.com/do5aglxsw/image/upload/v1690834278/mlops-final-project-bbc-clustering/1_ztivqa.png)



### 5.5 Use Prefect to do orchestration
Start the Prefect server using ```prefect server start```. Check out the dashboard at http://127.0.0.1:4200. 
```pipenv install prefect_aws```  Create and save artifacts to s3 bucket. 

Run the python code and the artifacts are saved in s3 buckets.
default artifacts URI: 's3://mflow-remote/1/95ff04c0e1a64edea415d5749d473e6f/artifacts'

![Flow](https://res.cloudinary.com/do5aglxsw/image/upload/v1690834278/mlops-final-project-bbc-clustering/3_ekn6jo.png)


### 5.6 Deploy the model in batch
Batch deployment. Fetch the model from s3 artifact. Feed the new data to the model and assign them the clusters. 
Build the docker image:
```shell
docker build -t mlops-zoomcamp-bbc-news-clustering:v1 .
```

### 5.7 Best practice
unit tests
    ```pipenv install --dev pytest```





