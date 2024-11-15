from openai import OpenAI
from tokens import project_key, org_key, openai_key 

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
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  
            messages= [
                {"role": "system", "content": "I want to take this text data and summarise it. I'm an investor looking to extract the most crucial information that I'll be later using to input to an opportunities tracker. I want 4 core datapoints: Name, Company Summary, Team Size, Requested Investment. In your output please format each of these on a new line. E.g. Name: [name] NEW LINE Company Summary: [summary] etc. Thanks!"},
                {"role": "user", "content": message}
            ],
        )
        return(process_openai_response(response))
