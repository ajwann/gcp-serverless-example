import functions_framework
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)

@functions_framework.http
def process_task(request):
    """
    Receives arguments and logs them.
    """
    try:
        request_json = request.get_json(silent=True)

        # This is the core requirement: Log the arguments
        logging.info(f"⚡ WORKER RUNNING! Received Arguments: {json.dumps(request_json)}")

        return 'Task Logged Successfully', 200
    except Exception as e:
        logging.error(f"Error: {e}")
        return 'Error processing task', 500
