import requests
import base64
from tokens import airtable_base_id, airtable_pat, airtable_table_name
from tenacity import retry, wait_exponential, stop_after_attempt

# Constants
DECK_FIELD = "fldtifmLhICjExfAZ"  # Replace with the actual field ID from Airtable
MAX_RETRIES = 5
MAX_BACKOFF = 10  # Maximum backoff time in seconds
MIME_TYPE = 'application/vnd.ms-powerpoint'  # MIME type for PowerPoint files
FILENAME = "Deck"  # Default filename used in the upload

# Retry logic applied to the top-level function
@retry(wait=wait_exponential(min=1, max=MAX_BACKOFF), stop=stop_after_attempt(MAX_RETRIES))
def send_to_airtable(data, file_path=None):
    """
    Main function to create a record in Airtable and optionally upload a file.
    
    Steps:
    1. Create a record in Airtable.
    2. If a file path is provided, upload the file directly to the created record.
    """
    # Step 1: Create the record
    record_id = create_record(data)
    
    # Step 2: Upload the file, if provided
    if file_path:
        upload_response = upload_file_to_airtable(record_id, file_path)
        return {"record_id": record_id, "upload_response": upload_response}

    return {"record_id": record_id}


def create_record(data):
    """
    Creates a record in Airtable and returns its ID.
    """
    url = f"https://api.airtable.com/v0/{airtable_base_id}/{airtable_table_name}"
    headers = {
        'Authorization': f'Bearer {airtable_pat}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while creating the record: {e}")
        raise

    if response.status_code in {200, 201}:
        record_id = response.json()['id']
        print(f"Record created successfully! Record ID: {record_id}")
        return record_id
    else:
        raise RuntimeError(f"Failed to create record. Status code: {response.status_code}")


def upload_file_to_airtable(record_id, file_path):
    """
    Uploads a file to a specified Airtable record field using the /uploadAttachment endpoint.
    """
    try:
        # Read and encode the file
        with open(file_path, 'rb') as file:
            file_content = file.read()
            file_base64 = base64.b64encode(file_content).decode('utf-8')

        # Prepare URL and headers for file upload
        file_upload_url = f"https://content.airtable.com/v0/{airtable_base_id}/{record_id}/{DECK_FIELD}/uploadAttachment"
        headers = {
            'Authorization': f'Bearer {airtable_pat}',
            'Content-Type': 'application/json'
        }

        # Prepare the upload payload
        upload_payload = {
            'contentType': MIME_TYPE,
            'file': file_base64,
            'filename': FILENAME
        }

        # Send the POST request to upload the file
        response = requests.post(file_upload_url, headers=headers, json=upload_payload)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Handle successful response
        if response.status_code in {200, 201}:
            print("File uploaded successfully.")
            return response.json()
        else:
            raise RuntimeError(f"File upload failed with status code {response.status_code}.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while uploading the file: {e}")
        raise
