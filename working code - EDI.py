import os
import re
# import datetime
import pandas as pd
import sys 


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
    pattern = r'BIG[*|]\d+[*|]([A-Za-z0-9]+)[*|]'  # Regex pattern to match BIG segment and invoice number 3rd
    matches = re.findall(pattern, edi_text)
    for match in matches:
        invoice_numbers.append(match)
    return invoice_numbers

def process_folders(parent_folder,client_name):
    """Iterates through folders and files, extracts invoice numbers, and creates Excel output.

    Args:
        parent_folder (str): The path to the parent folder containing year folders.
    """

    data = []
    for year_folder in os.listdir(parent_folder):
        year_path = os.path.join(parent_folder, year_folder)
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
                                        invoice_numbers = extract_invoice_numbers(edi_text)
                                        for invoice_number in invoice_numbers:
                                            data.append({
                                                "Invoice or CM Number": invoice_number,
                                                "File Name": filename,
                                                "Date": f"{year_folder}-{month_folder}-{day_folder}"
                                            })
                                    except FileNotFoundError:
                                        print(f"File not found: {file_path}")
                                    except PermissionError:
                                        print(f"Insufficient permissions to access: {file_path}")

    # Create Excel output if data is available
    if data:
        df = pd.DataFrame(data)
        print(df.head())
        df.to_excel(f"{client_name}_EDI_data.xlsx", index=False)
        print("Data saved , pls check parent folder! ")
    else:
        print("No EDI files found or no invoice numbers extracted.")

# Example usage
parent_folder = input("Give parent folder location: ")        
# parent_folder = "C:\\Users\\Omkar.sagavekar\\Downloads\\PROD invoice data 2023\\ABM 2023 Credit memo - EDI"  
client_name = input("Enter client name: ")
process_folders(parent_folder,client_name)

# when any key is pressed it will jump to sys.exit() 
input("Enter any key to quit.") 

# sys.exit() is used to make the program quits. ( duh ) 
sys.exit() 
