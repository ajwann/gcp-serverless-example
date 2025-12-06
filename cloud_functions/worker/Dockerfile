FROM python:3.13-slim
# Note: Using 3.13-slim. If 3.13.11 is strictly required and available, use python:3.13.11-slim

WORKDIR /app
COPY main.py .
RUN pip install functions-framework

# Cloud Functions 2nd Gen expects port 8080
CMD ["functions-framework", "--target=process_task", "--port=8080"]
