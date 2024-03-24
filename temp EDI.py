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
  pattern = r"BIG\*\d{8}\*(\d+)"
  matches = re.findall(pattern, edi_text)
  for match in matches:
    invoice_numbers.append(match)
  return invoice_numbers

# Example usage
with open("EDI ecol2.txt", "r") as f:
  edi_text = f.read()

invoice_numbers = extract_invoice_numbers(edi_text)

if invoice_numbers:
  print("Extracted invoice numbers:")
  for number in invoice_numbers:
    print(number)
else:
  print("No invoice numbers found in the EDI file.")
