# Telco Churn Prediction – Serverless ML on AWS Lambda

## **Overview**

This project implements a **Telco churn prediction system** using **machine learning**, deployed as a **serverless container on AWS Lambda**.  
It combines **ML inference, serverless backend, CI/CD, and cloud monitoring** to provide an automated and scalable prediction service.

---

## **Architecture**

![Architecture Diagram](https://github.com/AlFrancis-Dagaang/churn-prediction-frontend/blob/main/telco-churn-architecture.drawio.png?raw=true)  


- **Frontend:** Static website hosted on **S3 + CloudFront**

![Website Interface](https://github.com/AlFrancis-Dagaang/telecom-churn-prediction/blob/main/website-interface.png)



  
- **Backend:** **AWS Lambda container** running ML inference  
- **Database:** **DynamoDB** for storing predictions  
- **CI/CD:** GitHub Actions → Docker → ECR → Lambda  
- **Monitoring:** CloudWatch logs  

---

## **Features**

- Predict customer churn using a **Balanced Random Forest model**  
- Automatic **threshold adjustment** for classification  
- Scalable **serverless deployment** with Lambda  
- Stores predictions with timestamp and input data in **DynamoDB**  
- Frontend can consume API via **API Gateway**  

---

## **Tech Stack**

- **Backend / ML:** Python 3.10, Pandas, NumPy, Scikit-learn, Joblib, Imbalanced-learn  
- **Cloud Services:** AWS Lambda (container), API Gateway, DynamoDB, S3, CloudFront, CloudWatch, ECR  
- **CI/CD:** GitHub Actions + Docker  

---

## Setup / Deployment

### 1. GitHub Actions CI/CD

The workflow automatically builds the Docker image and deploys it to AWS Lambda:

- Checkout code from GitHub repository
- Configure AWS credentials (Access Key ID and Secret Access Key)
- Login to Amazon ECR
- Build, tag, and push Docker image to ECR
- Update the Lambda function with the new image
- Publish Lambda version for deployment

---

### 2. Docker

- Base image: `public.ecr.aws/lambda/python:3.10`
- Installs dependencies from `requirements.txt`
- Copies application code and ML model files into container
- Sets the Lambda handler to `app.lambda_handler`

---

### 3. Lambda Function (`app.py`)

- Loads pre-trained Balanced Random Forest model and threshold
- Optionally loads feature scaler for input data
- Converts incoming JSON request to a pandas DataFrame
- Aligns features to match model input and applies scaling if needed
- Calculates churn probability and determines prediction label (`CHURN` / `NOT CHURN`)
- Stores prediction, input data, timestamp, and unique ID in DynamoDB
- Returns JSON response with prediction details via API Gateway

---

### 4. Python Dependencies (`requirements.txt`)

The Lambda container requires the following Python packages:

- pandas
- numpy
- scikit-learn==1.7.1
- joblib
- boto3
- imbalanced-learn

---

## API Usage

- **Endpoint:** Configured through API Gateway → Lambda
- **Method:** POST
- **Request Body:** JSON containing customer attributes (e.g., gender, tenure, services)
- **Response:** JSON containing:

  - `predictionId`: Unique ID for the prediction
  - `churn_probability`: Probability value of churn
  - `prediction`: "CHURN" or "NOT CHURN"
  - `timestamp`: Unix timestamp of prediction

---

## Frontend Deployment

- Static files are deployed to S3 via GitHub Actions
- Served globally through CloudFront CDN

---

## Monitoring

- Lambda and API Gateway logs are sent to CloudWatch
- Monitor function executions, errors, and performance metrics

---

