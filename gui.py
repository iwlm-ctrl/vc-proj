# combined_file_picker.py

import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.scrolledtext import ScrolledText

def process_files(file_paths):
    """Process the list of file paths (for example, print them)."""
    if not file_paths:
        raise ValueError("No files were selected.")
    # Return a success message
    return file_paths

class FilePickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Picker")
        self.root.geometry("600x350")  
        self.root.resizable(False, False)

        self.file_paths = []  # List to store file paths

        # Label
        self.label = tk.Label(root, text="Select Files", font=('Helvetica', 14, 'bold'))
        self.label.pack(pady=10)

        # Select Files Button
        self.select_button = ttk.Button(root, text="Select Files", command=self.select_files)
        self.select_button.pack(pady=5)

        # ScrolledText widget to display file paths
        self.file_list_text = ScrolledText(root, width=60, height=8, wrap=tk.WORD, font=('Courier', 10))
        self.file_list_text.pack(pady=5)
        self.file_list_text.config(state=tk.DISABLED)

        # Submit Button
        self.submit_button = ttk.Button(root, text="Submit", command=self.submit_files)
        self.submit_button.pack(pady=10)

    def select_files(self):
        """Open file picker and allow multiple file selection"""
        files = filedialog.askopenfilenames(title="Select Files", 
                                            filetypes=(("All Files", "*.*"), ("Text Files", "*.txt"), ("CSV Files", "*.csv")))
        if files:
            self.file_paths = list(files)
            self.file_list_text.config(state=tk.NORMAL)
            self.file_list_text.delete(1.0, tk.END)
            self.file_list_text.insert(tk.END, "\n".join(self.file_paths))
            self.file_list_text.config(state=tk.DISABLED)

    def submit_files(self):
        """Submit the files for processing"""
        if self.file_paths:
            self.root.quit()  # Close the main loop when "Submit" is pressed

def run_file_picker():
    """Initialize the GUI, run the app, and return the selected file paths."""
    root = tk.Tk()
    app = FilePickerApp(root)
    root.mainloop()
    return app.file_paths  # Return file paths after GUI is closed