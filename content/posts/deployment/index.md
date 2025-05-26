+++
date = '2025-04-10T20:12:12+02:00'
draft = false
title = 'Deployment via Fast-API'
cover.image = "blog_deployment_ml_fastapi.webp"
cover.alt = "Verschiedene Services für das Deployment von ml-Modellen" #
cover.caption = "Deployment Services für ML-Modelle" 
cover.relative = true
tags = ["Deployment", "FastAPI", "Python", "Web Development", "API"] 
+++

## Introduction

In today's digital world, the deployment of applications is crucial for the success of a project. FastAPI has established itself as a powerful framework for developing APIs. In this article, we will explain the advantages and steps for deploying an application using FastAPI within the context of the loyalty project of Krombacher Brewery, and additionally highlight the suitability of FastAPI for deploying Machine Learning (ML) models.

## Functional Case

A functional version of the framework can be found in the loyalty project.

## Advantages of FastAPI

Using FastAPI offers numerous benefits:

- **Maximum Flexibility**: FastAPI allows for easy customization and extension of the API.
- **Better Performance**: Compared to Lambda functions, the cold start is eliminated, improving response times.
- **Swagger Documentation**: FastAPI automatically generates Swagger documentation for the endpoints, which includes various stages such as /health, /predict1, /predict2, etc.
- **Lower Costs**: No Sagemaker endpoint is required, reducing costs.
- **Better Monitoring**: All endpoints can be monitored within an ECS cluster.
- **Security Level**: HTTPS and x-api-key provide a comparable level of security.
- **Custom Domain**: The application can be operated in a specific "information-rich" domain.

## Why FastAPI for ML Models?

FastAPI is particularly well-suited for deploying Machine Learning models for several reasons:

1. **Asynchronous Processing**: FastAPI supports asynchronous programming, meaning requests can be processed in parallel. This is especially beneficial for ML models that often perform computationally intensive predictions.

2. **Easy Integration**: FastAPI easily integrates with popular ML libraries such as TensorFlow, PyTorch, and Scikit-Learn. This allows for seamless deployment of models as API endpoints.

3. **Rapid Development**: The use of Python types and automatic documentation generation speeds up the development process, which is advantageous for teams that need to respond quickly to changes.

4. **Validation and Serialization**: FastAPI provides built-in validation and serialization features that ensure the input data for ML models is correct before processing.

5. **Scalability**: FastAPI applications can be easily scaled using containerization (e.g., Docker) and orchestration tools (e.g., Kubernetes), which is essential for handling varying loads in ML applications.

## Prerequisites for Deployment

To use FastAPI for deploying ML models, several prerequisites are required:

- **Python Environment**: FastAPI requires Python 3.6 or higher.
- **ML Libraries**: Install the necessary ML libraries needed for your model (e.g., TensorFlow, PyTorch).
- **Docker**: Docker is required for containerizing the application.
- **Cloud Services**: If you want to deploy the application in the cloud, you need access to services like AWS, Azure, or Google Cloud.

## Weaknesses of FastAPI

Despite its many advantages, there are also some weaknesses to consider when using FastAPI:

1. **Learning Curve**: For developers new to asynchronous programming, the learning curve can be steep. It requires a certain understanding of asynchronous concepts.

2. **Performance Under Very High Loads**: While FastAPI is very performant for most applications, it may experience bottlenecks under extremely high loads (e.g., thousands of simultaneous requests) if the infrastructure is not scaled accordingly.

3. **Fewer Community Resources**: Compared to older frameworks like Flask or Django, there may be fewer community resources and plugins, which can make solving specific problems more challenging.

4. **Limited Built-in Features**: FastAPI focuses on being lightweight and fast, which means it may lack some built-in features that other frameworks provide, such as user authentication or database integration.

## Steps for Deployment

Here are the steps required for deploying a FastAPI application:

1. **Adjust FastAPI Script**: Customize the FastAPI script to meet your needs.

2. **Modify serverless.yml**: Change the points in the [serverless.yml](https://gitlab.com/krombacher-brauerei/datascience_krombacher/loyalty/-/blob/master/src/Fraud_Detection/serverless.yml) that are commented with "edit manually."

3. **Create Additional Elements**:
    - **ECS Cluster**: Create an ECS cluster to run the FastAPI application.
    - **securityGroupIds**:
        - Allow inbound traffic: Ports 80 (HTTP), 443 (HTTPS), 8000 (Load Balancer).
        - Outbound rules: Allow all IPv4 traffic.
    - **TaskRoleArn**: Adjust the policy in this role to control permissions within the FastAPI app.
    - **ExecutionRoleArn**: This role grants rights to access ECR, ECS, etc., for infrastructure creation.
    - **Adjust Ports**: Ensure that the container ports are adjusted according to the Docker container.
4. **Modify Dockerfile**: Adjust the [Dockerfile](https://gitlab.com/krombacher-brauerei/datascience_krombacher/loyalty/-/blob/master/src/Fraud_Detection/Dockerfile) to ensure that all dependencies and the ML model are correctly integrated.

5. **Build App Container**: Follow the steps to build, tag, log in, and push the container. This can be done using Docker commands such as `docker build`, `docker tag`, `docker login`, and `docker push`.

6. **Enter Container ARN**: Enter the container ARN in the serverless.yml under "resources->Resources->ECSTaskDefinition->Properties->ContainerDefinitions→Image".

7. **Perform Deployment**: Execute the command `sls deploy` to deploy the application in the cloud.

8. **Make Endpoint Available**: The endpoint is now available under the DNS of the load balancer and can be mapped to the "our" kbpim domain.

9. **Configure Route 53**:

    - Go to Hosted Zones.
    - Create a record.
    - Select record type A and enter the project name (future subdomain), enable alias.
    - Route traffic to the Application Load Balancer (ALB).
    - Choose simple routing.

## Architecture

The architecture of the application should be designed to support the aforementioned advantages and steps. A well-thought-out architecture enables efficient resource utilization and smooth interaction between the various components of the application.

## Conclusion

Deploying an application with FastAPI offers many advantages, including flexibility, performance, and cost efficiency. Especially for Machine Learning models, FastAPI is an excellent choice as it allows for rapid development and easy integration. Despite some weaknesses, such as the learning curve and performance under extreme loads, FastAPI remains a powerful tool for modern API development and the deployment of ML models.