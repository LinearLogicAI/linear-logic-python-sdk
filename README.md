
# Linear Logic Python SDK

This is the officially supported Python library for using Linear Logic's APIs.


## Installation

`pip install --upgrade linlog`

## Getting started

 1. [Initializing the client](#initializing-the-client)
 2. [Projects](#projects)
    1. [Batches](#batches)
    2. [Project Tasks](#project-tasks)
 3. [Datasets](#datasets)
    1. [Tasks](#dataset-tasks)
    2. [Model Runs](#model-runs)
 4. [Models](#models)

###Initializing the client

You can initialize a new client instance using your account credentials or an organisation-wide API token.

**From credentials**
```python
from linlog import LinLogClient

client = LinLogClient.init_from_credentials("email", "password")
```

**From token**
```python
from linlog import LinLogClient

client = LinLogClient.init_from_token("token")
```

###Projects

You can list all projects in your organisation or retrieve a specific project by its ID. Note: the ID of a project always starts with `p_` 

```python
# list all projects
projects = client.get_projects()

# get project by id
project = client.get_project("id")
```

####Batches

Batches allow you to partition the tasks within a project. Batches can tie to specific datasets you use internally, or can be used to note which tasks were part of a specific sprints for example  

You can list all batches within a project:

```python
# list all batches in a project
batches = client.get_project_batches("project_id")
```

####Project Tasks

Projects are a collection of tasks that require annotations or manual reviews. Tasks within a project can be retrieved as shown in the example below. There are multiple filters you can apply to the search, valid filters are: `limit`, `offset`, `status`, `created_date`, `created_date__gte`, `created_date__lte`, `created_date__gt`, `created_date__lt`, `complete`, `rejected`, `work_started`

```python
# example: get all completed tasks from a project
client.get_project_tasks(
    id="project_id",
    complete=True
)
```

###Datasets

Datasets are a collection of completed tasks and bring together your data, annotations and model predictions. Note: the ID of a dataset always starts with `d_` 

Retrieving datasets is much like retrieving projects:

```python
# list all datasets
datasets = client.get_datasets()

# get dataset by id
dataset = client.get_dataset("id")
```

####Dataset Tasks

Retrieving tasks from a dataset is identical to that of projects, the only exception is that the tasks are always complete and may have additional model runs attached to them.

```python
# example: get all tasks from a dataset
client.get_dataset_tasks("dataset_id")
```

####Model Runs

When you completed training a model you can start adding model runs to datasets. This allows you to generate key insights into the performance of your current model, but the results can also be used to compare the model with other models. 

Creating a model run is done as illustrated below:

```python
for (prediction, score) in predictions:
    # add each prediction to the model run
    client.create_model_run(dataset_id="dataset_id",
                            model_version_id="model_version_id",
                            task_id="task_id",
                            annotation=prediction,
                            confidence_score=score)
```

###Models

You can bring your own models to Linear Logic and use the platform to find the optimal model configuration. Learn how you can integrate your models with Linear Logic.

####Training models locally

```python
from linlog import ModelTrainer

# initialize trainer
trainer = ModelTrainer(client)

trainer.init(
    model_id="",
    version_name="",
    labels=[],
    config={
        "learning_rate": 0.01,
        "activation_function": "softmax",
        "batch_size": 256,
        "epochs": 10,
    }
)

epochs = 10
offset = random.random() / 5
for epoch in range(1, epochs):
    # Generate mock data
    acc = 1 - 2 ** -epoch - random.random() / epoch - offset
    loss = 2 ** -epoch + random.random() / epoch + offset

    # Store results, any key-value combination is valid
    trainer.log({"acc": acc, "loss": loss})

# Finish model training and start metrics generation
trainer.finish()
```

## Running unit test

Run: `python -m unittest tests/test_client.py`

## Building package

`python3 setup.py sdist bdist_wheel`

`python3 -m pip install dist/linlog-0.1-py3-none-any.whl --force-reinstall`