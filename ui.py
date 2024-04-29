import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from program import Program

class DataSharingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Privacy-Preserving Data Sharing Platform")
        self.master.geometry("600x400")  # Set window size
        self.master.configure(bg='#F8DDA4')  # Set window background color

        # Define colors from the palette
        self.brown = "#813405"
        self.red_orange = "#D45113"
        self.carrot_orange = "#F9A03F"
        self.peach_yellow = "#F8DDA4"
        self.tea_green = "#DDF9C1"

        # Create backend instance
        self.program = Program()

        # Create side-panel menu
        self.menu_frame = tk.Frame(master, bg=self.brown, width=150, height=400)
        self.menu_frame.grid(row=0, column=0, sticky="ns")

        # Upload button
        self.upload_button = tk.Button(self.menu_frame, text="Upload", font=("Helvetica", 14), bg=self.red_orange, fg="white", command=self.upload_file)
        self.upload_button.pack(fill="x", padx=20, pady=(30, 10))

        # Share button
        self.share_button = tk.Button(self.menu_frame, text="Share", font=("Helvetica", 14), bg=self.carrot_orange, fg="white", command=self.share_data)
        self.share_button.pack(fill="x", padx=20, pady=10)

        # Access button
        self.access_button = tk.Button(self.menu_frame, text="Access", font=("Helvetica", 14), bg=self.tea_green, fg="white", command=self.access_data)
        self.access_button.pack(fill="x", padx=20, pady=10)

        # Create space for displaying file list
        self.file_list_frame = tk.Frame(master, bg=self.peach_yellow, width=450, height=400)
        self.file_list_frame.grid(row=0, column=1, sticky="nsew")

        # Label to display relevant file list
        self.file_list_label = tk.Label(self.file_list_frame, text="", font=("Helvetica", 14), bg=self.peach_yellow, fg=self.brown)
        self.file_list_label.pack(padx=20, pady=20)

    # Function to handle file upload
    def upload_file(self):
        file_path = filedialog.askopenfilename()
        # Call backend method for file upload
        self.program.upload_file(file_path)
        # Update UI
        self.file_list_label.config(text="Uploaded file: " + file_path)

    # Function to handle data sharing
    def share_data(self):
        # Call backend method for data sharing
        self.program.share_data()
        # Update UI
        self.file_list_label.config(text="Shared data")

    # Function to access shared data
    def access_data(self):
        # Call backend method for accessing shared data
        self.program.access_data()
        # Update UI
        self.file_list_label.config(text="Accessed shared data")

def main():
    root = tk.Tk()
    app = DataSharingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
