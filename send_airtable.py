import requests
from tokens import airtable_base_id, airtable_pat, airtable_table_name
from tenacity import retry, wait_exponential, stop_after_attempt, RetryError

# Replace these with your actual Airtable Base ID and Personal Access Token
@retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(5))
def send_to_airtable(data):
    url = f"https://api.airtable.com/v0/{airtable_base_id}/{airtable_table_name}"

    headers = {
        "Authorization": f"Bearer {airtable_pat}",
        "Content-Type": "application/json"
    }

    # Send a POST request to create the new entry
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200 or response.status_code == 201:
        print("Record created successfully!")
        print("Response:", response.json())
        return response.json()
    else:
        print(f"Failed to create record. Status code: {response.status_code}")
        print("Error details:", response.json())
        raise RetryError(f"Error sending data to Airtable: {response.status_code}")
