import os
import xml.etree.ElementTree as ET
import pandas as pd
import sys 

# Base path to the root folder containing year folders
# base_path = input(r"Enter parent folder path: ")
base_path = r"InvoiceList_20240307010052_20240307010052"

print(base_path)

tree = ET.parse(base_path)
root = tree.getroot()

# invoice_data = []
# for table1 in root.iter('Table1'):
#     # Extract required information
#     print(table1)
#     invoice_number = table1.find('InvoiceNumber').text
#     po_number = table1.find('PONumber').text
#     item_description = table1.find('ItemDescription').text
#     quantity = table1.find('Quantity').text
#     unit_price = table1.find('UnitPrice').text
#     service_start_date = table1.find('ServiceStartDate').text
#     service_end_date = table1.find('ServiceEndDate').text
    
#     # Append extracted data to the list
#     invoice_data.append({
#         'InvoiceNumber': invoice_number,
#         'PONumber': po_number,
#         'ItemDescription': item_description,
#         'Quantity': quantity,
#         'UnitPrice': unit_price,
#         'ServiceStartDate': service_start_date,
#         'ServiceEndDate': service_end_date
#     })

table1 = root.find("Table1")

print(table1.find('InvoiceNumber').text)