import parse, send_airtable, summarise
from parse import extract_ppt_text
from summarise import summarise_content
from send_airtable import send_to_airtable
from gui import open_file_upload_gui  # Import the updated method

def main():
    # Launch the File Picker GUI and get the selected file paths (multi-select)
    file_paths = open_file_upload_gui()

    # Process or use the file paths as needed
    if file_paths:
        print("Selected files:")
        for path in file_paths:
            # Call the function for each file
            print(f"Processing file: {path}")
            
            # Step 1: Extract text from PPT file
            ppt_text = extract_ppt_text(path)
            print("Extracted text:")
            print(ppt_text)  # Print the extracted text for debugging
            
            # Step 2: Call OpenAI API to Summarize PPT content
            print("Starting summary generation...")
            ppt_summary = summarise_content(ppt_text)
            print("Summary:")
            print(ppt_summary)  # Print the summary for debugging

            # Step 3: Send Summarised content in JSON format to Airtable
            airtable_response = send_to_airtable(ppt_summary, file_path=path)
            print("Airtable Response:", airtable_response)
    else:
        print("No files were selected.")

if __name__ == "__main__":
    main()
