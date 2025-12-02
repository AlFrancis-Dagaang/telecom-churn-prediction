import joblib
import pandas as pd
import numpy as np
import json
import boto3
import uuid
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('churn-predictions')

def to_decimal(obj):
    if isinstance(obj, float):
        return Decimal(str(obj))
    if isinstance(obj, dict):
        return {k: to_decimal(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_decimal(v) for v in obj]
    return obj

model = joblib.load("balanced_rf_model.joblib")
threshold = joblib.load("brf_threshold.joblib")

try:
    scaler = joblib.load("scaler.joblib")
    use_scaler = True
except:
    use_scaler = False

def lambda_handler(event, context):
    body = json.loads(event["body"])
    df = pd.DataFrame([body])

    df_encoded = pd.get_dummies(df)
    df_aligned = df_encoded.reindex(columns=model.feature_names_in_, fill_value=0)

    X = scaler.transform(df_aligned) if use_scaler else df_aligned.values

    proba = float(model.predict_proba(X)[0][1])
    pred = 1 if proba >= threshold else 0
    prediction_label = "CHURN" if pred == 1 else "NOT CHURN"

    prediction_id = str(uuid.uuid4())
    timestamp = int(datetime.now().timestamp())

    item = {
        'predictionId': prediction_id,
        'timestamp': timestamp,
        'customerData': body,
        'churnProbability': round(proba, 4),
        'prediction': prediction_label,
        'createdAt': datetime.now().isoformat()
    }

    try:
        table.put_item(Item=to_decimal(item))
    except Exception as e:
        print(f"Error storing in DynamoDB: {e}")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "predictionId": prediction_id,
            "churn_probability": round(proba, 4),
            "prediction": prediction_label,
            "timestamp": timestamp
        })
    }
