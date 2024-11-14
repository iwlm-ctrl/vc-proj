import parse, send_airtable, summarise
from parse import extract_ppt_text
from summarise import summarise_content
from send_airtable import send_to_airtable
from file_upload_gui import open_file_upload_gui
def main():
    get_ppt_path = open_file_upload_gui()
    # Step 1: Extract text from PPT file
    ppt_text = extract_ppt_text(get_ppt_path)
    print("extracted text"+ppt_text)
    # Step 2: Call OpenAI API to Summarize PPT content
    print("LINE BREAK TO START SUMMARY FROM CHAT GPT")
    ppt_summary = summarise_content(ppt_text)
    print(ppt_summary)

    # Step 3: Send Summarised content in JSON format to Airtable
    airtable_response = send_to_airtable(ppt_summary)
    print("Airtable Response:", airtable_response)

if __name__ == "__main__":
    main()
