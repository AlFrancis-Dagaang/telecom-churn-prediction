# Telco Churn Prediction – Serverless ML on AWS Lambda

## **Overview**

This project implements a **Telco churn prediction system** using **machine learning**, deployed as a **serverless container on AWS Lambda**.  
It combines **ML inference, serverless backend, CI/CD, and cloud monitoring** to provide an automated and scalable prediction service.

---

## **Architecture**

![Architecture Diagram](https://github.com/AlFrancis-Dagaang/churn-prediction-frontend/blob/main/telco-churn-architecture.drawio.png?raw=true)  


- **Frontend:** Static website hosted on **S3 + CloudFront**  
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

## **Setup / Deployment**

### **1️⃣ GitHub Actions CI/CD**

The workflow automatically builds the Docker image and deploys it to AWS Lambda:

```yaml
# Key steps:
- Checkout code
- Configure AWS credentials


- Login to ECR
- Build, tag, and push Docker image
- Update Lambda function with new image
- Publish Lambda version
