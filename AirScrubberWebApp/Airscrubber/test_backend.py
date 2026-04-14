import os
import shutil
import tempfile
import sys

SOURCE_EXCEL_PATH = os.path.abspath("C:\\Users\\Dhruv Tavre\\.gemini\\antigravity\\Air Scrubber Altec working.xlsm")

temp_dir = tempfile.gettempdir()
temp_excel_path = os.path.join(temp_dir, "Temp_Air_Scrubber.xlsm")
shutil.copy2(SOURCE_EXCEL_PATH, temp_excel_path)

excel = None
wb = None
try:
    import pythoncom
    pythoncom.CoInitialize()
    
    import win32com.client as win32
    excel = win32.Dispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False
    print("Excel dispatched successfully.")
    
    wb = excel.Workbooks.Open(temp_excel_path)
    print("Workbook opened successfully.")
    ws = wb.Sheets("Summary")
    
    input_mapping = {
        "cfm": "D1", "ratio": "D2", "tankInside": "D4", 
        "workingPump": "D5", "standbyPump": "D6", "material": "D7", 
        "unitType": "D8", "ahuHeight": "D9", "ahuWidth": "D10"
    }
    data = {
        "cfm": "85000", "ratio": "6", "tankInside": "Yes", 
        "workingPump": "1", "standbyPump": "1", "material": "Stainless Steel", 
        "unitType": "50Coving", "ahuHeight": "3850", "ahuWidth": "5300"
    }
    
    for key, cell in input_mapping.items():
        if key in data and data[key] != "":
            val = data[key]
            try:
                val = float(val)
            except ValueError:
                pass
            ws.Range(cell).Value = val
            
    print("Inputs written. Calculating...")
    excel.Calculate()
    print("Calculated.")
    
    gpm = ws.Range("D3").Value
    print(f"GPM: {gpm}")
    
    for r in range(11, 13):
        sr_no = ws.Cells(r, 2).Value
        desc = ws.Cells(r, 3).Value
        print(f"Row {r} - Sr_no: {sr_no}, Desc: {desc}")
    
    wb.Close(SaveChanges=False)
    excel.Quit()
    print("All Good!")
except Exception as e:
    import traceback
    print("ERROR:", traceback.format_exc())
    if wb:
        try: wb.Close(SaveChanges=False)
        except: pass
    if excel:
        try: excel.Quit()
        except: pass
