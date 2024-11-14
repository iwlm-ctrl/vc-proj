import tkinter as tk
from tkinter import filedialog, messagebox
import time

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

def show_splash_screen(root):
    """Show the splash screen for 1 second."""
    splash = tk.Tk()
    splash.overrideredirect(True)  # Remove window borders
    splash.geometry("400x300")  # Set size of the splash screen
    
    splash_label = tk.Label(splash, text="LizzyWizard", font=("Helvetica", 32, "bold"))
    splash_label.pack(expand=True)

    # Optionally, add an image to the splash screen
    # splash_image = PhotoImage(file="splash_image.png")
    # splash_label = tk.Label(splash, image=splash_image)
    # splash_label.pack()

    splash.after(1000, splash.destroy)  # Close after 1 second
    splash.mainloop()

def open_file_upload_gui():
    """Function to open the file upload GUI and return the selected file path."""
    
    # Show the splash screen before starting the main application
    root_splash = tk.Tk()
    root_splash.withdraw()  # Hide the root window for the splash screen
    show_splash_screen(root_splash)

    # Now, open the main file upload GUI window
    root = tk.Tk()
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
