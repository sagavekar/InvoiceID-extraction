import os
import xml.etree.ElementTree as ET
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import re
from datetime import datetime


# Function to get folder names using dialog box
def select_folder():
    folder_selected = filedialog.askdirectory()  # Open folder selection dialog
    if folder_selected:
        folder_entry.delete(0, tk.END)  # Clear any previous input
        folder_entry.insert(
            tk.END, folder_selected
        )  # Insert selected folder path into entry field

# Function to get Invoice number out of cXML file
def getcXML():
    base_path = folder_entry.get()  # Get folder path from entry field
    client_name = client_entry.get()  # Get client name from entry field

    def directory_properties(base_path):
        # Check if directory exists
        if not os.path.exists(base_path):
            print("Directory does not exist.")
            return

        # Get properties
        file_count = 0
        for root, dirs, files in os.walk(base_path):
            file_count += len(files)

        print("Number of files in directory:", file_count)
        return file_count

    file_count = directory_properties(base_path)

    data = []

    # Iterate through year folders
    counter = 0
    for year_folder in os.listdir(base_path):
        year_path = os.path.join(base_path, year_folder)

        # Iterate through month folders within year folders
        for month_folder in os.listdir(year_path):
            month_path = os.path.join(year_path, month_folder)

            # Skip if it's not a directory: to ignoew desktop.ini system generated file
            if not os.path.isdir(month_path):
                continue

            # Iterate through day folders within month folders
            for day_folder in os.listdir(month_path):
                day_path = os.path.join(month_path, day_folder)

                # Process cXML files within day folders
                for filename in os.listdir(day_path):
                    if filename.endswith((".txt", ".xml")):
                        file_path = os.path.join(day_path, filename)

                        try:
                            tree = ET.parse(file_path)
                            # print(tree)
                            root = tree.getroot()
                            try:
                                invoiceID = root.find(
                                    "Request/InvoiceDetailRequest/InvoiceDetailRequestHeader"
                                ).attrib["invoiceID"]
                            except (KeyError, AttributeError):
                                invoiceID = None
                            # invoiceID = root.find("InvoiceHeader/InvoiceID").text if root.find("InvoiceHeader") is not None else None
                            try:
                                invoiceDate = root.find(
                                    "Request/InvoiceDetailRequest/InvoiceDetailRequestHeader"
                                ).attrib["invoiceDate"]
                            except:
                                invoiceDate = None
                            
                            try:
                                orderID = root.find("Request/InvoiceDetailRequest/InvoiceDetailOrder/InvoiceDetailOrderInfo/OrderIDInfo").attrib["orderID"]
                            except (KeyError, AttributeError):
                                orderID = None

                        except ET.ParseError:
                            print(f"Error parsing file: {file_path}")
                            continue

                        # Construct date string from folder structure
                        date_str = f"{year_folder}-{month_folder}-{day_folder}"

                        data.append(
                            {
                                "invoiceID": invoiceID,
                                "orderID" : orderID,
                                "invoiceDate": invoiceDate,
                                "invoiceFileName": file_path,
                                "date": date_str,
                            }
                        )
                        counter = counter + 1
                        print(f"{counter} / {file_count} ")

    # Create a DataFrame and export to Excel
    df = pd.DataFrame(data)
    print(df.head())
    df.to_excel(
        f"{client_name}_cXML_InvoiceData_{datetime.today().date()}.xlsx", index=False
    )

    os.startfile(
        f"{client_name}_cXML_InvoiceData_{datetime.today().date()}.xlsx"
    )  # this approach to open excel file is not reliable or cross-platform compatible.

# Function to get Invoice number out of EDI file
def getEDI():
    base_path = folder_entry.get()  # Get folder path from entry field
    client_name = client_entry.get()  # Get client name from entry field

    def extract_invoice_numbers(edi_text):
        """Extracts invoice numbers from an EDI X12 file using regular expressions.

        Args:
            edi_text (str): The EDI X12 file content as a string.

        Returns:
            list: A list of invoice numbers found in the EDI text.
        """
        # print(edi_text)
        invoice_numbers = []
        # pattern = r"BIG\*\d{8}\*(\d+)"  # Regex pattern to match BIG segment and invoice number 1st
        # pattern = r'BIG\*\d+\*([A-Za-z0-9]+)\*'  # Regex pattern to match BIG segment and invoice number 2nd
        pattern = r"BIG[*|]\d+[*|]([A-Za-z0-9]+)[*|]"  # Regex pattern to match BIG segment and invoice number 3rd
        matches = re.findall(pattern, edi_text)
        for match in matches:
            invoice_numbers.append(match)
        return invoice_numbers

    def process_folders(base_path, client_name):
        """Iterates through folders and files, extracts invoice numbers, and creates Excel output.

        Args:
            base_path (str): The path to the parent folder containing year folders.
        """

        data = []
        for year_folder in os.listdir(base_path):
            year_path = os.path.join(base_path, year_folder)
            if os.path.isdir(year_path):
                for month_folder in os.listdir(year_path):
                    month_path = os.path.join(year_path, month_folder)
                    if os.path.isdir(month_path):
                        for day_folder in os.listdir(month_path):
                            day_path = os.path.join(month_path, day_folder)
                            if os.path.isdir(day_path):
                                for filename in os.listdir(day_path):
                                    if filename.endswith(".txt"):
                                        file_path = os.path.join(day_path, filename)
                                        try:
                                            with open(file_path, "r") as f:
                                                edi_text = f.read()
                                            invoice_numbers = extract_invoice_numbers(
                                                edi_text
                                            )
                                            for invoice_number in invoice_numbers:
                                                data.append(
                                                    {
                                                        "Invoice or CM Number": invoice_number,
                                                        "File Name": file_path,
                                                        "Date": f"{year_folder}-{month_folder}-{day_folder}",
                                                    }
                                                )
                                        except FileNotFoundError:
                                            print(f"File not found: {file_path}")
                                        except PermissionError:
                                            print(
                                                f"Insufficient permissions to access: {file_path}"
                                            )

        # Create Excel output if data is available
        if data:
            df = pd.DataFrame(data)
            print(df.head())
            df.to_excel(
                f"{client_name}_EDI_InvoiceData_{datetime.today().date()}.xlsx",
                index=False,
            )
            print("Data saved , pls check parent folder! ")
            os.startfile(
                f"{client_name}_EDI_InvoiceData_{datetime.today().date()}.xlsx"
            )  # this approach is not reliable to open excel file or cross-platform compatible.
        else:
            print("No EDI files found or no invoice numbers extracted.")

    process_folders(
        base_path, client_name
    )  # calling process_folder  in order to exc. above two functions

# Function to get Invoice number out of CSV file
def getCSV():
    base_path = folder_entry.get()  # Get folder path from entry field
    client_name = client_entry.get()  # Get client name from entry field

    def directory_properties(base_path):
        # Check if directory exists
        if not os.path.exists(base_path):
            print("Directory does not exist.")
            return

        # Get properties
        file_count = 0
        for root, dirs, files in os.walk(base_path):
            file_count += len(files)

        print("Number of files in directory:", file_count)
        return file_count

    file_count = directory_properties(base_path)
    data = []

    # Iterate through year folders
    counter = 0
    for year_folder in os.listdir(base_path):
        year_path = os.path.join(base_path, year_folder)

        # Iterate through month folders within year folders
        for month_folder in os.listdir(year_path):
            month_path = os.path.join(year_path, month_folder)

            # Skip if it's not a directory: to ignoew desktop.ini system generated file
            if not os.path.isdir(month_path):
                continue

            # Iterate through day folders within month folders
            for day_folder in os.listdir(month_path):
                day_path = os.path.join(month_path, day_folder)

                # Process cXML files within day folders
                for filename in os.listdir(day_path):
                    # if filename.endswith((".txt", ".xml")):
                    file_path = os.path.join(day_path, filename)

                    try:
                        tree = ET.parse(file_path)
                        root = tree.getroot()
                        table1 = root.find("Table1")
                        table2 = root.find("Table2")

                        try:
                            InvoiceNumber = table1.find("InvoiceNumber").text
                        except (KeyError, AttributeError):
                            InvoiceNumber = None

                        try:
                            PONumber = table1.find("PONumber").text
                        except (KeyError, AttributeError):
                            PONumber = None

                        try:
                            ItemDescription = table1.find("ItemDescription").text
                        except (KeyError, AttributeError):
                            ItemDescription = None

                        try:
                            Quantity = table1.find("Quantity").text
                        except (KeyError, AttributeError):
                            Quantity = None

                        try:
                            UnitPrice = table1.find("UnitPrice").text
                        except (KeyError, AttributeError):
                            UnitPrice = None

                        try:
                            Amount = table2.find("Amount").text
                        except (KeyError, AttributeError):
                            Amount = None

                        try:
                            ServiceStartDate = table1.find("ServiceStartDate").text
                        except (KeyError, AttributeError):
                            ServiceStartDate = None

                        try:
                            ServiceEndDate = table1.find("ServiceEndDate").text
                        except (KeyError, AttributeError):
                            ServiceEndDate = None

                    except ET.ParseError:
                        print(f"Error parsing file: {file_path}")
                        continue

                    # Construct date string from folder structure
                    date_str = f"{year_folder}-{month_folder}-{day_folder}"

                    data.append(
                        {
                            "InvoiceNumber": InvoiceNumber,
                            "PONumber": PONumber,
                            "ItemDescription": ItemDescription,
                            "Quantity": Quantity,
                            "UnitPrice": UnitPrice,
                            "Amount": Amount,
                            "ServiceStartDate": ServiceStartDate,
                            "ServiceEndDate": ServiceEndDate,
                            "CreationDate": date_str,
                            "File name" : file_path
                        }
                    )
                    counter = counter + 1
                    print(f"{counter} / {file_count} ")

    # Create a DataFrame and export to Excel
    df = pd.DataFrame(data)
    print(df.head())
    # client_name = input("What is the client name?: ")
    df.to_excel(f"{client_name}_CSV_InvoiceData_{datetime.today().date()}.xlsx", index=False)
    os.startfile(f"{client_name}_CSV_InvoiceData_{datetime.today().date()}.xlsx")
    print("data saved, please check parent folder !")

# ------------ GUI Building------------------
   
# Create main window
root = tk.Tk()
root.title("Read Invoice V1.0 | Dev : Omkar Sagavekar - TSO")

# Invoice format selection (radio buttons)
invoice_format = (
    tk.IntVar()
)  # Integer variable to store selection (1 for cXML, 2 for EDI)

radio_cxml = tk.Radiobutton(root, text="cXML", variable=invoice_format, value=1)
radio_cxml.grid(row=3, column=0, padx=5, pady=5)

radio_edi = tk.Radiobutton(root, text="EDI", variable=invoice_format, value=2)
radio_edi.grid(row=3, column=1, padx=5, pady=5)

radio_edi = tk.Radiobutton(root, text="CSV", variable=invoice_format, value=3)
radio_edi.grid(row=3, column=2, padx=5, pady=5)

# Create and place other widgets (same as before)
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

process_button = tk.Button(
    root, text="Process", command=lambda: process_invoices(invoice_format.get())
)
# calling process_invoices(format_id) using Lambda so that it wont thrw declation missing
process_button.grid(row=2, column=1, padx=5, pady=5)


def process_invoices(format_id):
    if format_id == 1:
        getcXML()
    elif format_id == 2:
        getEDI()
    elif format_id == 3:
        getCSV()
    else:
        print("Please select an invoice format (cXML or EDI).")

# Run the application
root.mainloop()
