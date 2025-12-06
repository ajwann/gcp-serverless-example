from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import scheduler_v1
import datetime
import os

app = FastAPI()

# --- CONFIG ---

# Retrieve variables from the environment. Raise an error if they are not set.
PROJECT_ID = os.environ.get("PROJECT_ID")
WORKER_URL = os.environ.get("WORKER_URL")
SA_NAME = os.environ.get("SA_NAME", "app-scheduler-sa") # Default SA name

if not PROJECT_ID:
    raise ValueError("PROJECT_ID environment variable not set.")
if not WORKER_URL:
    raise ValueError("WORKER_URL environment variable not set.")

REGION = os.environ.get("REGION", "us-central1")

# The Service Account email is constructed from the PROJECT_ID and the SA_NAME
SERVICE_ACCOUNT_EMAIL = f"{SA_NAME}@{PROJECT_ID}.iam.gserviceaccount.com"


class TaskRequest(BaseModel):
    message: str
    delay_minutes: int

@app.post("/schedule-task")
def schedule_task(task: TaskRequest):
    """
    Creates a Cloud Scheduler job that hits the Worker Function.
    """
    client = scheduler_v1.CloudSchedulerClient()
    parent = f"projects/{PROJECT_ID}/locations/{REGION}"

    # SIMPLIFIED APPROACH for this example: 
    # We will create a job with a specific CRON schedule.
    run_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=task.delay_minutes)
    cron_schedule = f"{run_time.minute} {run_time.hour} * * *" # Runs once a day at this time

    job_name_suffix = f"task-{int(run_time.timestamp())}"
    job_name = f"{parent}/jobs/{job_name_suffix}"

    job = {
        "name": job_name,
        "schedule": cron_schedule,
        "time_zone": "UTC",
        "http_target": {
            "uri": WORKER_URL,
            "http_method": scheduler_v1.HttpMethod.POST,
            "body": f'{{"message": "{task.message}", "scheduled_for": "{run_time}"}}'.encode("utf-8"),
            "headers": {"Content-Type": "application/json"},
            # Add Auth Token so Scheduler can invoke the Worker securely
            "oidc_token": {
                "service_account_email": SERVICE_ACCOUNT_EMAIL,
                "audience": WORKER_URL
            }
        }
    }

    try:
        response = client.create_job(request={"parent": parent, "job": job})
        return {"status": "success", "job_name": response.name, "run_time": str(run_time)}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

# Add CORS (Cross-Origin Resource Sharing) so your React app can hit this
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to your Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
