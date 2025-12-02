import joblib
import pandas as pd
import numpy as np
import json
import boto3
import uuid
from datetime import datetime

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('churn-predictions')

# Load models from local container (bundled in Docker image)
model = joblib.load("balanced_rf_model.joblib")
threshold = joblib.load("brf_threshold.joblib")
try:
    scaler = joblib.load("scaler.joblib")
    use_scaler = True
except:
    use_scaler = False

def lambda_handler(event, context):
    # Parse input
    body = json.loads(event["body"])
    
    # Make prediction
    df = pd.DataFrame([body])
    df_encoded = pd.get_dummies(df)
    df_aligned = df_encoded.reindex(columns=model.feature_names_in_, fill_value=0)

    if use_scaler:
        X = scaler.transform(df_aligned)
    else:
        X = df_aligned.values

    proba = model.predict_proba(X)[0][1]
    pred = 1 if proba >= threshold else 0
    prediction_label = "CHURN" if pred == 1 else "NOT CHURN"
    
    # Generate unique ID and timestamp
    prediction_id = str(uuid.uuid4())
    timestamp = int(datetime.now().timestamp())
    
    # Store in DynamoDB
    try:
        table.put_item(
            Item={
                'predictionId': prediction_id,
                'timestamp': timestamp,
                'customerData': body,
                'churnProbability': round(float(proba), 4),
                'prediction': prediction_label,
                'createdAt': datetime.now().isoformat()
            }
        )
        print(f"Successfully stored prediction {prediction_id} in DynamoDB")
    except Exception as e:
        print(f"Error storing in DynamoDB: {str(e)}")
        # Continue even if DynamoDB fails
    
    # Return response
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "predictionId": prediction_id,
            "churn_probability": round(float(proba), 4),
            "prediction": prediction_label,
            "timestamp": timestamp
        })
    }