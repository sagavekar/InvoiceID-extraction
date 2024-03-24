import tkinter as tk
from PIL import Image, ImageTk  # For image handling

class InvoiceReaderGUI:
    def __init__(self, master):
        self.master = master
        master.title("Read cXML Invoice | Dev: Omkar Sagavekar-TSO")

        # Configure window appearance (optional, customize to your preference)
        self.master.configure(bg="#34495e")  # Background color

        # Create and place widgets
        self.create_widgets()

        # Animation (optional, example provided)
        self.logo_animation()  # Call the animation function

    def create_widgets(self):
        # Labels with custom styling
        self.folder_label = tk.Label(
            self.master, text="Folder Path:", font=("Arial", 12, "bold"), fg="white", bg="#34495e"
        )
        self.folder_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.client_label = tk.Label(
            self.master, text="Client Name:", font=("Arial", 12, "bold"), fg="white", bg="#34495e"
        )
        self.client_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Entries with improved styling
        self.folder_entry = tk.Entry(self.master, width=50, font=("Arial", 12), bg="#e0e0e0")
        self.folder_entry.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.client_entry = tk.Entry(self.master, width=50, font=("Arial", 12), bg="#e0e0e0")
        self.client_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # Buttons with custom styling and hover effects
        self.select_button = tk.Button(
            self.master,
            text="Select Folder",
            command=self.select_folder,
            font=("Arial", 12, "bold"),
            bg="#2980b9",
            fg="white",
            activebackground="#2471a3",  # Hover effect background color
            activeforeground="white",  # Hover effect text color
            relief="raised",  # Button border style
            borderwidth=2,
        )
        self.select_button.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        self.process_button = tk.Button(
            self.master,
            text="Process",
            command=self.getcXML,
            font=("Arial", 12, "bold"),
            bg="#2980b9",
            fg="white",
            activebackground="#2471a3",
            activeforeground="white",
            relief="raised",
            borderwidth=2,
        )
        self.process_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

    def select_folder(self):
        pass

    def getcXML(self):
        pass