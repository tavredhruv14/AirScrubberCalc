import openpyxl
import re

print("Loading original workbook...")
wb = openpyxl.load_workbook(r'C:\Users\Dhruv Tavre\.gemini\antigravity\Air Scrubber Altec working.xlsm', data_only=False)

# delete the faulty formulas
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str) and cell.value.startswith('='):
                if 'http' in cell.value or '[MM60' in cell.value:
                    # just clear it to avoid formulas crashing
                    cell.value = 0

print("Saving clean workbook...")
wb.save('Clean_Air_Scrubber.xlsx')
print("Done!")
