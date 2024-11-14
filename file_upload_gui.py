import tkinter as tk
from tkinter import filedialog, messagebox

class FileUploadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Upload App")
        self.root.geometry("400x300")

        # Path variable to store the file path
        self.file_path = None

        # Label to show file selection area
        self.drop_label = tk.Label(root, text="Click 'Select File' to choose a .pptx file", relief="solid", width=40, height=10)
        self.drop_label.pack(padx=20, pady=20)

        # Button to open file dialog
        self.select_button = tk.Button(root, text="Select File", command=self.select_file)
        self.select_button.pack(pady=10)

        # Submit button to confirm file upload
        self.submit_button = tk.Button(root, text="Submit", command=self.submit_file)
        self.submit_button.pack(pady=10)

    def select_file(self):
        """Open file dialog to select .pptx file."""
        self.file_path = filedialog.askopenfilename(
            filetypes=[("PowerPoint files", "*.pptx")],
            title="Select a .pptx file"
        )
        if self.file_path:
            # Update label to show the selected file name
            self.drop_label.config(text=f"File selected: {self.file_path.split('/')[-1]}")
        else:
            # Reset label if no file is selected
            self.drop_label.config(text="No file selected.")

    def submit_file(self):
        """Submit the file path when the user clicks the submit button."""
        if self.file_path:
            self.root.quit()  # Close the window after selecting the file
        else:
            messagebox.showwarning("No file", "Please select a .pptx file before submitting.")

    def get_file_path(self):
        """Return the file path once the file is uploaded."""
        return self.file_path

def open_file_upload_gui():
    """Function to open the file upload GUI and return the selected file path."""
    root = tk.Tk()  # Create the root window for the main GUI

    # Now, open the main file upload GUI window
    app = FileUploadApp(root)

    # Start the Tkinter event loop and wait for the user to select and submit a file
    root.mainloop()

    # Return the file path once the window is closed
    return app.get_file_path()

# Example call to start the file upload process
if __name__ == "__main__":
    file_path = open_file_upload_gui()
    if file_path:
        print(f"File selected: {file_path}")
    else:
        print("No file selected.")
