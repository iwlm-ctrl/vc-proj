import requests
from tokens import airtable_base_id, airtable_pat, airtable_table_name

# Replace these with your actual Airtable Base ID and Personal Access Token
def send_to_airtable(data):
    # Define the URL for the Airtable API endpoint for the Issues table
    url = f"https://api.airtable.com/v0/{airtable_base_id}/{airtable_table_name}"

    # Set up the headers with the authorization token
    headers = {
        "Authorization": f"Bearer {airtable_pat}",
        "Content-Type": "application/json"
    }

    # Send a POST request to create the new entry
    response = requests.post(url, headers=headers, json=data)

    # Check and print the response to see if it was successful
    if response.status_code == 200 or response.status_code == 201:
        print("Record created successfully!")
        print("Response:", response.json())
    else:
        print("Failed to create record.")
        print("Status code:", response.status_code)
        print("Error details:", response.json())
