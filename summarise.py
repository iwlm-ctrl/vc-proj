from openai import OpenAI
from tokens import project_key, org_key, openai_key, user_fields

# make a client
openai = OpenAI(
    api_key=openai_key
)

def process_openai_response(response):
    # Extract the content of the message from the first choice
    content = response.choices[0].message.content.strip()  # Use dot notation to access content
    
    # Initialize a dictionary to hold the parsed data
    return_data = {"fields": {}}
    
    # Split the content into lines
    lines = content.split("\n")
    
    # Iterate over the lines and extract key-value pairs
    for line in lines:
        if ": " in line:
            key, value = line.split(": ", 1)
            return_data["fields"][key.strip()] = value.strip()
    
    return return_data

#### try assistant
def summarise_content(message):
        # Make a test request to OpenAI's chat model to confirm access
        print("Using these user fields:\n",user_fields)
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  
            messages= [
                {"role": "system", "content": f"I want to take this text data and summarise it. I'm an investor looking to extract the most crucial information that I'll be later using to input to an opportunities tracker. I'm interested in these core datapoints: {user_fields}. Interpret the deck to create high-quality answers for each of the datapoints. In your output please print the datapoint field name as a key-value pair. Separate each datapoint with a new line. Thanks!"},
                {"role": "user", "content": message}
            ],
        )
        return(process_openai_response(response))
