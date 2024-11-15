import tkinter as tk
from tkinter import filedialog, messagebox
import os

class FileUploadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Upload App")
        self.root.geometry("400x300")
        self.root.resizable(False, False)  # Prevent resizing for faster rendering

        # List variable to store multiple file paths
        self.file_paths = []

        # Label to show file selection area
        self.drop_label = tk.Label(root, text="Click 'Select Files' to choose .pptx files", width=40)
        self.drop_label.pack(padx=10, pady=20)

        # Button to open file dialog
        self.select_button = tk.Button(root, text="Select Files", command=self.select_files)
        self.select_button.pack(pady=5)

        # Submit button to confirm file upload
        self.submit_button = tk.Button(root, text="Submit", command=self.submit_files)
        self.submit_button.pack(pady=5)

    def select_files(self):
        """Open file dialog to select .pptx files (multi-select)."""
        files = filedialog.askopenfilenames(
            filetypes=[("PowerPoint files", "*.pptx")],
            title="Select .pptx files",
            initialdir=os.getcwd()  # Start in current directory for faster access
        )
        if files:
            self.file_paths = list(files)
        self.update_label()

    def update_label(self):
        """Update label text based on file selection."""
        if self.file_paths:
            filenames = "\n".join(os.path.basename(f) for f in self.file_paths)  # Show file names only
            self.drop_label.config(text=f"Files selected:\n{filenames}")
        else:
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
    root = tk.Tk()
    app = FileUploadApp(root)
    root.mainloop()
    return app.get_file_paths()
