<a href="https://explosion.ai"><img src="https://linearlogic.ai/images/logo-small.png" width="20" style="margin-top: 20px;" align="right" /></a>

# Linear Logic Python SDK

This is the officially supported Python library for using Linear Logic's APIs.


## 📖 Installation

Install the SDK using PIP:

`pip install --upgrade git+https://github.com/linearlogicai/linear-logic-python-sdk.git`

## 💡 Getting started

 1. [Quickstart](#quickstart)
 2. [Initializing the client](#initializing-the-client)
 3. [Organisations](#organisations)
 4. [Projects](#projects)
    1. [Batches](#batches)
    2. [Project Tasks](#project-tasks)
    3. [Project Workflows](#project-workflows)
 5. [Datasets](#datasets)
    1. [Dataset Tasks](#dataset-tasks)
    2. [Model Runs](#model-runs)
 6. [Models](#models)

## 🚀 Quickstart

### 1. Create a categorisation project 
```python
from linlog import LinLogClient

client = LinLogClient.init_from_token("token")

# Create project
cat_project = client.create_project(
    title="Categorisation Project", 
    project_type="categorisation", 
    objects_to_annotate=[
        { "label": "Positive", "task_type": "categorisation" },
        { "label": "Negative", "task_type": "categorisation" }
    ]
)

# Add task to project
client.create_categorisation_task(
    cat_project['id'], 
    "Every Star Wars release is amazing!"
)
```

### 2. Remove completed tasks 
```python
from linlog import LinLogClient

client = LinLogClient.init_from_token("token")

# Get the first available project
cat_project = client.get_projects()[0]

# Retrieve all completed tasks
tasks = client.get_project_tasks(
    id=cat_project['id'],
    complete=True
)

while tasks.offset + tasks.limit < tasks.count + 1:
    # Perform removal
    client.delete_tasks([t['id'] for t in tasks])
    
    # Get next tasks
    tasks = client.get_project_tasks(
        id=cat_project['id'],
        complete=True,
        offset=tasks.offset + tasks.limit
    )
```

# SDK Instructions

## Initializing the client

You can initialize a new client instance using your account credentials or an organisation-wide API token.

### From credentials
```python
from linlog import LinLogClient

client = LinLogClient.init_from_credentials("email", "password")
```

### From token
```python
from linlog import LinLogClient

client = LinLogClient.init_from_token("token")
```

## Organisations

All users are registered to one organisation. To retrieve all groups and members registered to the organisation simply call the `get_organisation()` function. It doesn't require any parameters because all users are registered to exactly one organisation. Therefore the organisation corresponding to the user can be derived from the authentication.

```python
client.get_organisation()
```

## Projects

Projects can be created from the dashboard or programmatically from the API. The following example shows the creation of an image project which allows annotating cats with polygons.

```python
client.create_project(
    title="Sample Project", 
    project_type="image", 
    objects_to_annotate=[{ "label": "Cat", "task_type": "polygon" }]
)
```

You can list all projects in your organisation or retrieve a specific project by its ID. Note: the ID of a project always starts with `p_` 

```python
# list all projects
projects = client.get_projects()

# get project by id
project = client.get_project("id")
```



Project are also easily deleted from their ID. Be aware that deleting a project will also delete all associated tasks with it.

```python
client.delete_project("project_id")
```

#### Batches

Batches allow you to partition the tasks within a project. Batches can tie to specific datasets you use internally, or can be used to note which tasks were part of a specific sprints for example  

You can list all batches within a project:

```python
# list all batches in a project
batches = client.get_project_batches("project_id")
```

#### Project Tasks

Tasks can be created programmatically using the API. The following example creates a categorisation task with the text *"Hello, world"*.

```python
# sample categorisation task
client.create_categorisation_task("project_id", "Hello, world")
```

Categorisation tasks take four valid attachment types: `image`, `text`, `iframe` and `html`. If the attachment type is left blank the attachment will automatically be interepeted as text.

```python
# specify attachment type
client.create_categorisation_task(
    "project_id",
    attachment="<strong>Hi!</strong>",
    attachment_type="html"
)
```

You can also pre-annotate the tasks by setting the annotations attribute.

```python
# pre-annotated annotations
client.create_categorisation_task(
    "project_id", 
    attachment="Paris", 
    annotations=[{ "label": "Location", "task_type": "categorisation" }]
)

# auto-complete task
client.create_categorisation_task(
    "project_id",
    "This task does not require annotating",
    complete=True
)

```

Eventually you may wish to archive and delete the tasks. Simply obtain the IDs of the tasks you wish to remove and call the `delete_tasks` function.

```python
client.delete_tasks(["task_id_1", "task_id_2"])
```


Projects are a collection of tasks that require annotations or manual reviews. Tasks within a project can be retrieved as shown in the example below. There are multiple filters you can apply to the search, valid filters are: `limit`, `offset`, `status`, `created_date`, `created_date__gte`, `created_date__lte`, `created_date__gt`, `created_date__lt`, `complete`, `rejected`, `work_started`

```python
# example: get all completed tasks from a project
tasks = client.get_project_tasks(
    id="project_id",
    complete=True
)
```

The `get_project_tasks` returns a `Paginator` instance. This allows to get the current offset, limit and total count from the request.
- The offset gives the offset of the current resultset.
- The limit shows the maximum number of instances returned from a single request.
- The count gives the total number of instances present in the entire resultset.

The offset, limit and value can be accessed as properties from the Paginator:
> `(tasks.offset, tasks.limit, tasks.count)`

#### Project Workflows



### Datasets

Datasets are a collection of completed tasks and bring together your data, annotations and model predictions. Note: the ID of a dataset always starts with `d_` 

Retrieving datasets is much like retrieving projects:

```python
# list all datasets
datasets = client.get_datasets()

# get dataset by id
dataset = client.get_dataset("id")
```

#### Dataset Tasks

Retrieving tasks from a dataset is identical to that of projects, the only exception is that the tasks are always complete and may have additional model runs attached to them.

```python
# example: get all tasks from a dataset
client.get_dataset_tasks("dataset_id")
```

#### Model Runs

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

### Models

You can bring your own models to Linear Logic and use the platform to find the optimal model configuration. Learn how you can integrate your models with Linear Logic.

#### Training models locally

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