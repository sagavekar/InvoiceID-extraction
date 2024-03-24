import os
import xml.etree.ElementTree as ET
import pandas as pd
import sys

# Base path to the root folder containing year folders
# base_path = input(r"Enter parent folder path: ")
base_path = r"C:\SET-TSO\Python Projects\python code to get invoiceID\CSV sample files"


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
                    }
                )
                counter = counter + 1
                print(f"{counter} / {file_count} ")

# Create a DataFrame and export to Excel
df = pd.DataFrame(data)
print(df.head())
client_name = input("What is the client name?: ")
df.to_excel(f"{client_name}_invoice_data.xlsx", index=False)
os.startfile(f"{client_name}_invoice_data.xlsx")
print("data saved, please check parent folder !")

# when any key is pressed it will jump to sys.exit()
input("Enter any key to quit.")

# sys.exit() is used to make the program quits. ( duh )
sys.exit()
