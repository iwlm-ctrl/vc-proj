import parse, send_airtable, summarise
from parse import extract_ppt_text
from summarise import summarise_content
from send_airtable import send_to_airtable
from gui import run_file_picker

def main():
# Launch the File Picker GUI and get the selected file paths
    file_paths = run_file_picker()

    # Process or use the file paths as needed
    if file_paths:
        print("Selected files:")
        for path in file_paths:
            # call the function for each
            print(path)
            # Step 1: Extract text from PPT file
            ppt_text = extract_ppt_text(path)
            print("extracted text"+ppt_text)
            # Step 2: Call OpenAI API to Summarize PPT content
            print("LINE BREAK TO START SUMMARY FROM CHAT GPT")
            ppt_summary = summarise_content(ppt_text)
            print(ppt_summary)

            # Step 3: Send Summarised content in JSON format to Airtable
            airtable_response = send_to_airtable(ppt_summary)
            print("Airtable Response:", airtable_response)
        print("Success")
    else:
        print("No files were selected.")
    
if __name__ == "__main__":
    main()
