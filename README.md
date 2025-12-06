This is a vibe-coded example app of a serverless app on Google Cloud Platform with a React front-end. I've recorded the prompts used to generate this example app in the `/prompts` directory

Architecture Overview

* Frontend (Vite + React): Users sign up/login and input task details (message + time).
* Auth (Firebase): Handles user identity securely.
* Backend (Cloud Run - Python 3.13): An API that authenticates requests and creates "Cloud Scheduler" jobs.
* Worker (Cloud Function V2 - Python 3.13): The target that runs the task. It receives the arguments and logs them.
