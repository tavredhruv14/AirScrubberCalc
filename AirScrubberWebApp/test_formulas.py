import formulas
import traceback
import sys

print("Loading...")
sys.stdout.flush()
try:
    fpath = r"C:\Users\Dhruv Tavre\.gemini\antigravity\Air Scrubber Altec working.xlsm"
    xl_model = formulas.ExcelModel().loads(fpath).finish()
    
    inputs = {
        "'[Air Scrubber Altec working.xlsm]Summary'!D1": 6000,
        "'[Air Scrubber Altec working.xlsm]Summary'!D2": 2,
        "'[Air Scrubber Altec working.xlsm]Summary'!D4": "Yes",
        "'[Air Scrubber Altec working.xlsm]Summary'!D5": 1,
        "'[Air Scrubber Altec working.xlsm]Summary'!D6": 1,
        "'[Air Scrubber Altec working.xlsm]Summary'!D7": "PP",
        "'[Air Scrubber Altec working.xlsm]Summary'!D8": "Vertical",
        "'[Air Scrubber Altec working.xlsm]Summary'!D9": 2000,
        "'[Air Scrubber Altec working.xlsm]Summary'!D10": 1000
    }
    
    print("Calculating...")
    sys.stdout.flush()
    res = xl_model.calculate(
        outputs=[
            "'[Air Scrubber Altec working.xlsm]Summary'!E21",
            "'[Air Scrubber Altec working.xlsm]Summary'!G10"
        ],
        inputs=inputs
    )
    print("Result:")
    print(res)
    sys.stdout.flush()
except Exception as e:
    print("Error:", e)
    traceback.print_exc()
