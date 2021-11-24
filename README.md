##### This repo is for creating pipeline using Kubeflow and steps to get deployed in GCP

Components are different stages in Machine Learning like pre-processing, training.. and each has its own .py file..

We have to create .yaml files for different components (.py) using kfp (Kubeflow pipeline) - we will be using @component decorator.

We can then take all .yaml files and create .JSON file (we will be using @pipeline decorator) for providing it to cloud provider.

##### Deploying to GCP

We have individual components and we created .yaml for all those.

We took all .yaml and created final JSON for pipeline.

we also manually create one JSON file for passing parameters, we have raw inputs in this parameter JSON, outputs flow from component to component wont be here.

We need the below services

- Cloud Function

- Cloud Scheduler

- Cloud Storage

- Cloud Source Repo

- Cloud Pub/Sub Topic



##### What is cloud function?

Cloud Function are serverless - Event Driven Architecture (EDA)

What is Serverless (Function as a Service - FAAS) ? - It has servers, but we are not responsible for managing and provisioning of these servers.

1 - Pay for execution means no idle time means we don't have permanent servers and it goes idle when we are not using it.

2 - cost efficient

3 - Auto scalable

4 - Faster time to market (FTM) - since we are not responsible for any of the management and deployment of any underlying infrastructure.

5 - Highly available - cloud providers takes care of fault tolerance

Usually cloud-function subscribed to the topic.

Whenever topics receives the message, our cloud function event gets triggered.



##### What is cloud scheduler ?

We can schedule to run cloud functions at a specific point in time or on a time interval.

We can trigger jobs by either sending data payload to HTTP Endpoint or we can send it to a pub/sub channel. 

This cloud-scheduler sends message to the topic, since our cloud function subscribed to that topic, cloud function event gets triggered and in turn it runs the pipeline.



##### What is Cloud Pub/Sub - Publisher/Subscriber Model ?

What is Pub/Sub ? 

Pub/Sub is an asynchronous messaging service that decouples services that produce events from services that process events.

Pub/Sub is an asynchronous communication method which messages are exchanged between applications without knowing the identity of sender or recipient.

Cloud Pub/Sub lets users focus on application logic, regardless of location or scale. It includes end-to-end encryption and audit logging, fully automated scaling and provisioning with virtually unlimited throughput.

##### It is asynchronous communication - means does not require immediate response.

Publisher publishes messages to the topics available.

Subscribes receives messages based on the topic subscribed.



##### Cloud Source Repo

When we complete our development, we push our code to cloud source repo.



##### Cloud Build - for CI/CD 

So as we know, when we do change our code and do git push, our cloud function has to be called to redeploy, to achieve that, we need to use something called Cloud Build.

In the cloud build :

we will give cloud build name, description.

Event : example - push to a branch

Source : Our repo path, in our case it is cloud source repo.

Branch : our repo branch

Included files filter - thailand_pipelines/train/** (means whenever there is a change here)

Configuration : we have to mention what it has to refer like cloud build configuration file (yaml or json)

or docker or buildpacks.

In our case, we are mentioning Cloud Build configuration file 

and location is that cloud-function-build.yaml file (refer below)



##### Cloud Storage - Artifacts storage

When we created pipeline JSON, we used .py file which uses .yaml files to create final JSON.

In that .py file, we mentioned like below :

-----------------------------------------------------------------------------------------------------------------------------------------------------------

@pipeline(

  name='clusters-scoring-pipeline',

  description='Clustering models scoring pipeline.',



  \# needs to be changed based on region/project

  pipeline_root='gxxx/vertex_ai_pipelines_root'

)

-----------------------------------------------------------------------------------------------------------------------------------------------------------

##### This pipeline root is the place where you want to store your artifacts, that is cloud storage.



##### Workflow Details

To run on every interval :

we created cloud function using cloud-function-build yaml file, to run our pipeline using cloud-scheduler.

It will trigger our pipeline (trigger_CS_scoring_pipeline) and exit, it will not wait for the execution to get completed.

our cloud function has been subscribed to topic, so cloud scheduler sends the message to the topic, and our cloud function event gets triggered and it runs our pipeline

Below is the cloud-function-build yaml file.

-----------------------------------------------------------------------------------------------------------------------------------------------------------

steps:

 \# Deploying/Updating Cloud Function to trigger Customer Segmentation training pipeline

 \- name: "gcr.io/cloud-builders/gcloud"

  args:

   \- functions

   \- deploy

   \- customer-segmentation-scoring-pipeline-trigger

   \- --region=europe-west3

   \- --memory=512MB

   \- --runtime=python39

   \- --trigger-topic=customer-segmentation-scoring-pipeline-topic

   \- --service-account=gfr-cd-d-acc-dsteam-svc01@ul-cd-d-902533-ai-th-prj.iam.gserviceaccount.com

   \- --source=https://source.developers.google.com/projects/ul-cd-d-902533-ai-th-prj/repos/customer-segmentation/moveable-aliases/dev/paths/thailand_pipelines/train

   \- --entry-point=trigger_CS_scoring_pipeline

-----------------------------------------------------------------------------------------------------------------------------------------------------------

##### Yaml file details:

trigger-topic : Cloud function gets redeployed whenever this pub/sub topic receives message, it calls that entry-point function, so runs the pipeline.

Cloud-Scheduler sends message to the topic.

entry-point : same, it runs our pipeline.

Below is entry-point function we have in our main.py file.

##### main.py file details:

It has the code to run our pipeline.

It uses both JSONs created.

It uses kfp APIs like below.

-----------------------------------------------------------------------------------------------------------------------------------------------------------

from kfp.v2.google.client import AIPlatformClient

api_client = AIPlatformClient(

   project_id="123",

   region="xyz"

)

-----------------------------------------------------------------------------------------------------------------------------------------------------------

It also has that entry-point function like below.

-----------------------------------------------------------------------------------------------------------------------------------------------------------

def trigger_CS_scoring_pipeline(event,context):

​	"logic.."

  response = api_client.create_run_from_job_spec(

​    job_spec_path='clusters_scoring_pipeline.json',

​    enable_caching = False,

​    parameter_values=clusters_parameters,

​    service_account='gfr-cd-d-acc-dsteam-svc01@ul-cd-d-902533-ai-th-prj.iam.gserviceaccount.com'

  )

-----------------------------------------------------------------------------------------------------------------------------------------------------------



Vertex AI

We can see the pipeline like Azure ML Studio.

The pipeline present is from the create run method in our main.py file, which is pipeline..





##### Cloud Monitoring

It is monitoring logs.

Lets say cloud function subscribed to pub/sub topic.

So based on the pub/sub topic message, we can create logs from our cloud function, like security logs or general info logs.

Then cloud monitor will monitor the logs and if its security log, it will alert to the mail id.

##### cloud function

##### Based on the message posted on that pub/sub topic, this function works.

##### It creates logs...

import base64

import json

def hello_pubsub(event, context):

​	“”Triggered from a message on a Cloud Pub/Sub topic.

​	Args:

​		event (dict): Event payload.

​		context (google.cloud.function.Context): Metadata for the event.

​	pubsub_message = base64.b64decode(event[‘data’]).decode(‘utf-8’)

​	print(pubsub_message)

​	if pubsub_message==‘some_error_line’:

​		entry = dict(

​				severity=‘ALERT’,

​				message=‘Some failure occurred’

​	)

​	else:

​		entry = dict(

​				severity=‘INFO’,

​				message=‘This is the default display msg’

​	)

​	print(json.dumps(entry))



##### Cloud Monitor

##### For creating alert based on the logs cloud function logged.

resource.type=‘cloud_function’

severity=ALERT

log_name=‘projects/xxx’

resource.labels.project_id=‘playground-xxx’

resource.labels.function_name=‘test-function’

