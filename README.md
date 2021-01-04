# iris-model

Many Machine Learning engineers want to deploy machine learning models for real-time inference, and pay only for what they use. Using Amazon EC2 instances, Fargate containers or SageMaker Inference for real-time inference may not be cost effective to support sporadic inference requests throughout the day.
At re:Invent 2020, AWS announced an update for AWS Lambda. Now you can easily build and deploy larger workloads that rely on larger dependencies, such as machine learning or data intensive workloads. Functions deployed as container images benefit from the same operational simplicity, automatic scaling, high availability, and native integrations with many services. The best part is that a custom Dockerfile could either extend a lambda base image, provided by AWS or use custom base images.

In our example we will be hosting a model trained using Iris Data Set (http://archive.ics.uci.edu/ml/datasets/iris). The data set contains 3 classes of 50 instances each, where each class refers to a type of iris plant.

- app.py file loads trained model and runs prediction to determine the iris class type based on the inference request payload data.
- requirments.txt - contains the correct versions of the required Python libraries (or “packages”) to run the Python code we’ve written.
- Dockerfile - contains instructions needed to build the image. 
- iris_trained_model.pkl - our trained model

Take model, requirments.txt and app.py and package them as Docker container. 

Before we proceed, make sure you have the following prerequisites installed and configured on your local machine:
Docker CLI 
AWS CLI

We will need to use Docker runtime itself to prepare the docker image and then AWS CLI to push our new image to AWS ECR service to be used by Lambda.
First, let's create a Dockerfile to build the container image for our Lambda function, starting from the AWS provided base image for the python3.7x runtime. 

All AWS provided base images are available in Docker Hub and ECR Public. In this case, we are using the base image hosted in ECR Public.
The Dockerfile above is adding the inference source code (app.py) and the files describing the packages and the dependencies (requirements.txt) to the base image. Then, runs pip to install the dependencies. We set the CMD to the function handler, but this could also be done later as a parameter override when configuring the Lambda function.
I used the Docker CLI to build the iris-trained-model container image locally:
$ docker build -t iris-inference-image .

To check if this is working, start the container image locally using the Lambda Runtime Interface Emulator:
$ docker run -p 9000:8080 iris-inference-image:latest

Now, test a function invocation with cURL. Here, I am passing a sample payload:
$ curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '[5.7,2.8,4.5,1.3]'

To upload the container image, I create a new ECR repository in my account and tag the local image to push it to ECR:
$ aws ecr create-repository --repository-name iris-inference-image --image-scanning-configuration scanOnPush=true

Authenticate the Docker CLI to your Amazon ECR registry:
$ aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AccountID>.dkr.ecr.us-east-1.amazonaws.com
    
Tag your image to match your repository name:
$docker tag iris-inference-image:latest <AccountID>.dkr.ecr.us-east-1.amazonaws.com/iris-inference-image:latest
    
And deploy the image to Amazon ECR using the docker push command:
$docker push <AccountID>.dkr.ecr.us-east-1.amazonaws.com/iris-inference-image
    
I am using the AWS Management Console to complete the creation of the function. You can also use the AWS Serverless Application Model (SAM), that has been updated to add support for container images.
In the Lambda console, click on Create function. Select Container image, give the function a name, and then Browse images to look for the right image in my ECR repositories.

After I select the repository, I use the latest image I uploaded. You can update the image to use in the function code. Updating the function configuration has no impact on the image used, even if the tag was reassigned to another image in the meantime.
Optionally, I can override some of the container image values.
When lambda function is deployed, we can test it. In the Lambda console, go to the detail page of our function, and select Configure test events from the test events dropdown (the dropdown beside the orange test button). In the dialog box, you can manage 10 test events for your function. First past the test payload (base64 encoded) in the dialog box (e.g. { "body": "WzUuMSwzLjUsMS40LDAuMl0="}) and type the event name.
Choose "Create". After test event is saved, you can see iris-model test data in the Test list. Click on "Test" button.

Now let's add the API Gateway as trigger. In the Lambda console, go to the Designer view and select "Add Trigger" and add the API Gateway using an HTTP API. Select "Open" for security mechanism for your API endpoint for simplicity. Click "Add". Under API Gateway details, we can see the API Endpoint.
Now we are ready to send an POST HTTP request to the API Gateway endpoint. We can use Curl command with API endpoint to test out lambda function:
$curl -XPOST "https://<endpoint-id>.execute-api.us-east-1.amazonaws.com/default/iris-prediction" -d '[5.1,3.5,1.4,0.2]'
It works!
This is how final solution looks like:
    
Happy Machine Learning!
