

## Problem statement

For the project, we will ask you to build an end-to-end ML project. 


* Dataset was downloaded from [BBC-News Data on Kaggle](https://www.kaggle.com/datasets/gpreda/bbc-news). 
* I want to use K-Means to do clustering. 

Environment 

* Create a conda environment and activate

```shell
conda create -n mlops-env

conda activate mlops-env
```

* Install libraries
```shell
pipenv install mlflow scikit-learn prefect pandas boto3 sentence-transformers seaborn
```

* Activate the virtual environment, run
```shell
pipenv shell
```

* Show the path of  the virtual env, run ```pipenv --venv```
/Users/xiahe/.local/share/virtualenvs/mlops-final-project-70huLeJa 
* Set the python interpreter in VS code. ctrl+shift+p -> choose python interpreter -> add the python above /Users/xiahe/.local/share/virtualenvs/mlops-final-project-70huLeJa/**bin/python**


* Train a model on that dataset tracking your experiments
K-means clustering
use ```mlflow ui```, open http://127.0.0.1:5000 to see all your experiments. 
If you are satisfied with one model, you can register model. 

* Create a model training pipeline
```pipenv install --dev jupyter_contrib_nbextensions```  
To turn the notebook into a script, use```jupyter nbconvert --to script bbc_news_clustering.ipynb```. 
Convert the code into different tasks using prefect to orchestrate the whole pipeline.

1. Read data
2. Do embedding
3. Prepare input matrix for KMeans model
4. Clustering with Kmeans
5. Experiment tracking with AWS EC2 as tracking server host, save artifacts to AWS S3. 

Start the Prefect server using ```prefect server start```. Check out the dashboard at http://127.0.0.1:4200. 
```pipenv install prefect_aws```  Create and save artifacts to s3 bucket. 

* Deploy the model in batch, web service or streaming

* Monitor the performance of your model


* Follow the best practices 


## Technologies 

You don't have to limit yourself to technologies covered in the course. You can use alternatives as well:

* Cloud: AWS, GCP, Azure or others
* Experiment tracking tools: MLFlow, Weights & Biases, ... 
* Workflow orchestration: Prefect, Airflow, Flyte, Kubeflow, Argo, ...
* Monitoring: Evidently, WhyLabs/whylogs, ...
* CI/CD: Github actions, Gitlab CI/CD, ...
* Infrastructure as code (IaC): Terraform, Pulumi, Cloud Formation, ...



* Problem description
    * 0 points: Problem is not described
    * 1 point: Problem is described but shortly or not clearly 
    * 2 points: Problem is well described and it's clear what the problem the project solves
* Cloud
    * 0 points: Cloud is not used, things run only locally
    * 2 points: The project is developed on the cloud OR the project is deployed to Kubernetes or similar container management platforms
    * 4 points: The project is developed on the cloud and IaC tools are used for provisioning the infrastructure
* Experiment tracking and model registry
    * 0 points: No experiment tracking or model registry
    * 2 points: Experiments are tracked or models are registred in the registry
    * 4 points: Both experiment tracking and model registry are used
* Workflow orchestration
    * 0 points: No workflow orchestration
    * 2 points: Basic workflow orchestration
    * 4 points: Fully deployed workflow 
* Model deployment
    * 0 points: Model is not deployed
    * 2 points: Model is deployed but only locally
    * 4 points: The model deployment code is containerized and could be deployed to cloud or special tools for model deployment are used
* Model monitoring
    * 0 points: No model monitoring
    * 2 points: Basic model monitoring that calculates and reports metrics
    * 4 points: Comprehensive model monitoring that send alerts or runs a conditional workflow (e.g. retraining, generating debugging dashboard, switching to a different model) if the defined metrics threshold is violated
* Reproducibility
    * 0 points: No instructions how to run code at all
    * 2 points: Some instructions are there, but they are not complete
    * 4 points: Instructions are clear, it's easy to run the code, and the code works. The version for all the dependencies are specified.
* Best practices
    * [ ] There are unit tests (1 point)
    * [ ] There is an integration test (1 point)
    * [ ] Linter and/or code formatter are used (1 point)
    * [ ] There's a Makefile (1 point)
    * [ ] There are pre-commit hooks (1 point)
    * [ ] There's a CI/CD pipeline (2 points)



