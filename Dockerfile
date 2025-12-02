FROM public.ecr.aws/lambda/python:3.10

# Copy requirements and install
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt --target ${LAMBDA_TASK_ROOT}

# Copy application code
COPY app.py ${LAMBDA_TASK_ROOT}

# Copy model files (bundled in container)
COPY balanced_rf_model.joblib ${LAMBDA_TASK_ROOT}
COPY brf_threshold.joblib ${LAMBDA_TASK_ROOT}
COPY scaler.joblib ${LAMBDA_TASK_ROOT}

CMD ["app.lambda_handler"]