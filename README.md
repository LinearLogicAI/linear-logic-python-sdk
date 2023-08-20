<a href="https://explosion.ai"><img src="https://linearlogic.ai/images/logo-small.png" width="20" style="margin-top: 50px;" align="right" /></a>

# Linear Logic Python SDK

This is the officially supported Python library for using Linear Logic's APIs.


## 📖 Installation

Install the SDK using PIP:

`pip install --upgrade linearlogic`

## 💡 Getting started

1. [Quickstart](#quickstart)
2. [SDK Instructions](#sdk-instructions)
    1. [Initializing the client](#initializing-the-client)
    2. [Organisations](#organisations)
    3. [Projects](#projects)
        1. [Batches](#batches)
        2. [Project Tasks](#project-tasks)
        3. [Project Workflows](#project-workflows)
    4. [Datasets](#datasets)
        1. [Dataset Tasks](#dataset-tasks)
        2. [Model Runs](#model-runs)
    5. [Models](#models)
    6. [Exporting data](#exporting-data)
    7. [Importing data](#importing-data-from-local-files)
    8. [Serialization](#serialization)
    9. [Deserialization](#deserialization)
3. [CLI Guide](#cli-guide)

## 🚀 Quickstart

### 1. Create an image project

The steps below show how to create a minimalistic image project for instance segmentation purposes. Two labels are added to the project (cats and dogs) plus one sample image task is created.

```python
from linlog import LinLogClient
from linlog.schemas import Project, ImageTask

client = LinLogClient.init_from_token("token")

# Create project
project = Project.create(
    client,
    project_title="My new project",
    project_type="image"
)

# Set project's taxonomy
project.create_labels(client, [
    { "name": "cat", "task_type": "polygon" },
    { "name": "dog", "task_type": "polygon" }
])

# Add a task to the project
project.create_task(client, new ImageTask(
    attachment="https://xyz.com/image.png",
    attachment_type="image"
))

# If you don't want to store the image on our servers and host it externally, use:
project.create_task(client, new ImageTask(
    attachment="https://xyz.com/image.png",
    attachment_type="image",
    external_data=True
))
```

The newly created project is now accessible in the platform and one image will be awaiting labeling.

### 2. Remove completed tasks

```python
from linlog import LinLogClient
from linlog.schemas import Project

client = LinLogClient.init_from_token("token")
project = Project.get_by_id(client, 'project_id')

# Retrieve all completed tasks
tasks = project.get_tasks(
    client,
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

### Global authentication
`$ linlog.authenticate`

You can initialize a new client instance using your account credentials or an organisation-wide API token.

### Authenticate with credentials
```python
from linlog import LinLogClient

client = LinLogClient.init_from_credentials("email", "password")
```

### Token authentication
```python
from linlog import LinLogClient

client = LinLogClient.init_from_token("token")
```

## Organisations

All users are registered to one organisation. To retrieve all groups and members registered to the organisation simply call the `get()` function from the Organisation model. It doesn't require any parameters because all users are registered to exactly one organisation. Therefore the organisation corresponding to the user can be derived from the authentication.

```python
from linlog.schemas import Organisation
Organisation.get()
```

## Projects

Projects can be created from the dashboard or programmatically from the API. The following example shows the creation of an image project which allows annotating cats with polygons.

```python
from linlog import LinLogClient
from linlog.schemas import Project, ImageTask

client = LinLogClient.init_from_token("token")

# Create project
project = Project.create(
    client,
    project_title="My new project",
    project_type="image"
)

# Set project's taxonomy
project.create_labels(client, [
    { "name": "cat", "task_type": "polygon" },
    { "name": "dog", "task_type": "polygon" }
])
```

You can list all projects in your organisation or retrieve a specific project by its ID. Note: the ID of a project always starts with `p_`

```python
# list all projects
projects = Project.get_all(client)

# get project by id
project = Project.get_by_id(client, "id")
```

Project are also easily deleted from their ID. Be aware that deleting a project will also delete all associated tasks with it.

```python
Project.delete(client, "project_id")
```

#### Batches

Batches allow you to partition the tasks within a project. Batches can tie to specific datasets you use internally, or can be used to note which tasks were part of a specific sprints for example

You can list all batches within a project:

```python
# list all batches in a project
project = Project.get_by_id(client, "id")
batches = project.get_batches(client)
```

#### Project Tasks

Tasks can be created programmatically using the API. The following example creates a categorisation task with the text *"Hello, world"*.

```python
# sample categorisation task
project.create_task(
    client,
    new CategorisationTask(
        attachment='Hello, world',
        attachment_type='text'
    )
)
```

Categorisation tasks take four valid attachment types: `image`, `text`, `iframe` and `html`. If the attachment type is left blank the attachment will automatically be interepeted as text.

```python
# specify attachment type
project.create_task(
    client,
    new CategorisationTask(
        attachment='<strong>Hi!</strong>',
        attachment_type='html'
    )
)
```

You can also pre-annotate the tasks by setting the annotations attribute.

```python
# pre-annotated annotations
client.create_categorisation_task(
    "project_id",
    attachment="Paris",
    annotations=[{ "name": "Location", "task_type": "categorisation" }]
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
project = Project.get_by_id(client, 'id')
tasks = project.get_tasks(
    complete=True
)
```

The `get_tasks` returns a `Paginator` instance. This allows to get the current offset, limit and total count from the request.
- The offset gives the offset of the current resultset.
- The limit shows the maximum number of instances returned from a single request.
- The count gives the total number of instances present in the entire resultset.

The offset, limit and value can be accessed as properties from the Paginator:
> `(tasks.offset, tasks.limit, tasks.count)`

#### Project Workflows


## Datasets

Datasets are a collection of completed tasks and bring together your data, annotations and model predictions. Note: the ID of a dataset always starts with `d_`

Retrieving datasets is much like retrieving projects:

```python
# list all datasets
from linlog.schemas import Dataset
datasets = Dataset.get_all()

# get dataset by id
dataset = Dataset.get_by_id("id")
```

### Dataset Tasks

Retrieving tasks from a dataset is identical to that of projects, the only exception is that the tasks are always complete and may have additional model runs attached to them.

```python
# example: get 10 tasks from a dataset
dataset = Dataset.get_by_id('...')
10_tasks = dataset.get_tasks(limit=10)
```

### Model Runs

When you completed training a model you can start adding model runs to datasets. This allows you to generate key insights into the performance of your current model, but the results can also be used to compare the model with other models.

Creating a model run is done as illustrated below:

```python
for (prediction, score) in predictions:
    # add each prediction to the model run
    client.create_model_run(
        dataset_id="dataset_id",
        model_version_id="model_version_id",
        task_id="task_id",
        annotation=prediction,
        confidence_score=score
    )
```

## Exporting data

Valid data formats are: linearlogic (default), cvat, coco, yolo.

```python
from pathlib import Path
from linlog.exporter import get_exporter, export_tasks

exporter = get_exporter('coco')
tasks = dataset.get_tasks()

export_tasks(
  exporter,
  tasks,
  Path('./my-local-folder')
)
```

## Importing data from local files

Valid data formats are: linearlogic (default), cvat, coco, yolo.

```python
from linlog.importer import get_importer, import_tasks

importer = get_importer('cvat')
files = [
    './dataset-1/cvat-data.xml',
    './dataset-2/cvat-data.xml',
    ...
]

tasks = import_tasks(
    importer,
    files
)
```

## Serialization

```python
dataset_dict = dataset.to_dict()
assert type(dataset_dict) is dict
```

```python
project.to_dict()
task.to_dict()
annotation.to_dict()
```

## Deserialization

```python
dataset_dict = dataset.to_dict()
assert type(dataset_dict) is dict
```

```python
project.to_dict()
task.to_dict()
annotation.to_dict()
```


# CLI guide

| **Action**            | **Command**                  |
|-----------------------|------------------------------|
| Global authentication | `$ linlog authenticate`      |
| List all datasets     | `$ linlog datasets`          |
| Dataset info          | `$ linlog dataset-info [id]` |
| Pull task data        | `$ linlog pull-dataset [id]` |
| List all projects     | `$ linlog projects`          |
| Project info          | `$ linlog project-info [id]` |

## Running unit test

Run: `python -m unittest tests/test_client.py`

## Building package

`python3 setup.py sdist bdist_wheel`

`python3 -m pip install dist/linlog-0.1-py3-none-any.whl --force-reinstall`