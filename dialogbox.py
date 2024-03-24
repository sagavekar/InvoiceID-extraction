import tkinter as tk

def select_folder():
    folder_selected = tk.filedialog.askdirectory()  # Open folder selection dialog
    if folder_selected:
        folder_entry.delete(0, tk.END)  # Clear any previous input
        folder_entry.insert(tk.END, folder_selected)  # Insert selected folder path into entry field

def process_input():
    base_path = folder_entry.get()  # Get folder path from entry field
    client_name = client_entry.get()  # Get client name from entry field
    # Perform processing with base_path and client_name
    print("Folder path:", base_path)
    print("Client name:", client_name)

# Create main window
root = tk.Tk()
root.title("Read cXML Invoice | Dev: Omkar Sagavekar-TSO")

# Create and place widgets
folder_label = tk.Label(root, text="Folder Path:")
folder_label.grid(row=0, column=0, padx=5, pady=5)

folder_entry = tk.Entry(root, width=50)
folder_entry.grid(row=0, column=1, padx=5, pady=5)

select_button = tk.Button(root, text="Select Folder", command=select_folder)
select_button.grid(row=0, column=2, padx=5, pady=5)

client_label = tk.Label(root, text="Client Name:")
client_label.grid(row=1, column=0, padx=5, pady=5)

client_entry = tk.Entry(root, width=50)
client_entry.grid(row=1, column=1, padx=5, pady=5)

process_button = tk.Button(root, text="Process", command=process_input)
process_button.grid(row=2, column=1, padx=5, pady=5)

# Run the application
root.mainloop()
