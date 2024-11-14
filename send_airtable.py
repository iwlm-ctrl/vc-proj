import requests
import base64
from tokens import airtable_base_id, airtable_pat, airtable_table_name
from tenacity import retry, wait_exponential, stop_after_attempt, RetryError

# Constants
DECK_FIELD = "fldtifmLhICjExfAZ"  # Ensure this matches the exact field name in Airtable
MAX_RETRIES = 5
MAX_BACKOFF = 10  # Maximum backoff time in seconds
MIME_TYPE = 'application/vnd.ms-powerpoint'  # MIME type for PowerPoint files
FILENAME = "Deck"  # Placeholder for the file name

@retry(wait=wait_exponential(min=1, max=MAX_BACKOFF), stop=stop_after_attempt(MAX_RETRIES))
def upload_file_to_airtable(record_id, file_path):
    """Uploads a file to Airtable and returns the file URL."""
    try:
        with open(file_path, 'rb') as file:
            file_content = file.read()
            file_base64 = base64.b64encode(file_content).decode('utf-8')

        # Prepare URL and headers
        file_upload_url = f"https://content.airtable.com/v0/{airtable_base_id}/{record_id}/{DECK_FIELD}/uploadAttachment"
        headers = {
            'Authorization': f'Bearer {airtable_pat}',
            'Content-Type': 'application/json'
        }

        # Prepare payload
        upload_payload = {
            'contentType': MIME_TYPE,
            'file': file_base64,
            'filename': FILENAME
        }

        # Send the POST request
        response = requests.post(file_upload_url, headers=headers, json=upload_payload)
        response.raise_for_status()  # Raise exception for 4xx/5xx responses

        # Parse and handle the response
        return handle_file_upload_response(response)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while uploading the file: {e}")
        raise RetryError(f"Error uploading file to Airtable: {e}")

def handle_file_upload_response(response):
    """Handles the response from Airtable after file upload."""
    if response.status_code in {200, 201}:
        response_json = response.json()
        fields = response_json.get('fields', {})

        # Check if the file was successfully uploaded
        if DECK_FIELD in fields:
            attachments = fields[DECK_FIELD]
            if isinstance(attachments, list) and attachments:
                file_url = attachments[0].get('url')
                if file_url:
                    print(f"File uploaded successfully. File URL: {file_url}")
                    return file_url
        print(f"Field '{DECK_FIELD}' not found in response.")
        raise RetryError(f"Error uploading file to Airtable: Missing '{DECK_FIELD}' field in response.")

    else:
        print(f"Failed to upload file. Status code: {response.status_code}")
        print("Error details:", response.json())
        raise RetryError(f"Error uploading file to Airtable: {response.status_code}")

def send_to_airtable(data, file_path=None):
    """Creates a record in Airtable and uploads a file if provided."""
    url = f"https://api.airtable.com/v0/{airtable_base_id}/{airtable_table_name}"
    headers = {
        'Authorization': f'Bearer {airtable_pat}',
        'Content-Type': 'application/json'
    }

    # Step 1: Create the record without the file
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while creating the record: {e}")
        raise RetryError(f"Error creating record in Airtable: {e}")

    if response.status_code in {200, 201}:
        record_id = response.json()['id']
        print(f"Record created successfully! Record ID: {record_id}")
    else:
        print(f"Failed to create record. Status code: {response.status_code}")
        raise RetryError(f"Error creating record in Airtable: {response.status_code}")

    # Step 2: Upload the file (if a file path is provided)
    if file_path:
        file_url = upload_file_to_airtable(record_id, file_path)

        # Step 3: Update the record with the file URL in the 'Deck' field
        return update_record_with_file(record_id, file_url)

    return response.json()

def update_record_with_file(record_id, file_url):
    """Updates the Airtable record with the file URL."""
    url = f"https://api.airtable.com/v0/{airtable_base_id}/{airtable_table_name}/{record_id}"
    headers = {
        'Authorization': f'Bearer {airtable_pat}',
        'Content-Type': 'application/json'
    }

    update_payload = {
        "fields": {DECK_FIELD: [{"url": file_url}]}  # Add the file URL to the Deck field
    }

    try:
        update_response = requests.patch(url, headers=headers, json=update_payload)
        update_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while updating the record with the file: {e}")
        raise RetryError(f"Error updating record in Airtable: {e}")

    if update_response.status_code in {200, 201}:
        print("Record updated with the file in the 'Deck' field successfully!")
        return update_response.json()
    else:
        print(f"Failed to update record. Status code: {update_response.status_code}")
        raise RetryError(f"Error updating record in Airtable: {update_response.status_code}")
