import re

def extract_invoice_numbers(edi_text):
  """
  Extracts invoice numbers from an EDI X12 file using regular expressions.

  Args:
      edi_text (str): The EDI X12 file content as a string.

  Returns:
      list: A list of invoice numbers found in the EDI text.
  """
  invoice_numbers = []
  # Regex pattern to match the BIG segment followed by the invoice number
  first_line = edi_text.split('~')[0].strip()
  print(first_line)
  if re.search(r'KUBDUKEENERGYOH\|01\|101496735P', first_line):
    print("aaaa")
    pattern = r'REF\|12\|([a-zA-Z0-9]+)~'
    matches = re.findall(pattern, edi_text)
    for match in matches:
      invoice_numbers.append(match)
    return invoice_numbers
  else:
    pattern = r"BIG[*|]\d+[*|]([A-Za-z0-9]+)[*|]" 
    matches = re.findall(pattern, edi_text)
    for match in matches:
      invoice_numbers.append(match)
    return invoice_numbers

# Example usage
with open(r"C:\SET-TSO\Python Projects\python code to get invoiceID\EDI Duke invoice sample.txt", "r") as f:
  edi_text = f.read()

invoice_numbers = extract_invoice_numbers(edi_text)

if invoice_numbers:
  print(len(invoice_numbers))
  print("Extracted invoice numbers:")
  for number in invoice_numbers:
    print(number)  
else:
  print("No invoice numbers found in the EDI file.")
