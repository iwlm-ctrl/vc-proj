import tkinter as tk
from tkinter import filedialog, messagebox

class FileUploadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Upload App")
        self.root.geometry("400x300")

        # List variable to store multiple file paths
        self.file_paths = []

        # Label to show file selection area
        self.drop_label = tk.Label(root, text="Click 'Select Files' to choose .pptx files", relief="solid", width=40, height=10)
        self.drop_label.pack(padx=20, pady=20)

        # Button to open file dialog
        self.select_button = tk.Button(root, text="Select Files", command=self.select_files)
        self.select_button.pack(pady=10)

        # Submit button to confirm file upload
        self.submit_button = tk.Button(root, text="Submit", command=self.submit_files)
        self.submit_button.pack(pady=10)

    def select_files(self):
        """Open file dialog to select .pptx files (multi-select)."""
        files = filedialog.askopenfilenames(
            filetypes=[("PowerPoint files", "*.pptx")],
            title="Select .pptx files"
        )
        if files:
            self.file_paths = list(files)
        self.update_label()

    def update_label(self):
        """Update label text based on file selection."""
        if self.file_paths:
            # Display the selected file names in the label
            filenames = "\n".join([f.split('/')[-1] for f in self.file_paths])  # Show file names only
            self.drop_label.config(text=f"Files selected:\n{filenames}")
        else:
            # Reset label if no files are selected
            self.drop_label.config(text="No files selected.")

    def submit_files(self):
        """Submit the file paths when the user clicks the submit button."""
        if self.file_paths:
            self.root.quit()  # Close the window after selecting the files
        else:
            messagebox.showwarning("No files", "Please select at least one .pptx file before submitting.")

    def get_file_paths(self):
        """Return the list of file paths once the files are uploaded."""
        return self.file_paths

def open_file_upload_gui():
    """Function to open the file upload GUI and return the selected file paths."""
    root = tk.Tk()  # Create the root window for the main GUI
    
    # Now, open the main file upload GUI window
    app = FileUploadApp(root)

    # Start the Tkinter event loop and wait for the user to select and submit files
    root.mainloop()

    # Return the selected file paths once the window is closed
    return app.get_file_paths()

# Example call to start the file upload process
if __name__ == "__main__":
    file_paths = open_file_upload_gui()
    if file_paths:
        print(f"Files selected: {file_paths}")
    else:
        print("No files selected.")
