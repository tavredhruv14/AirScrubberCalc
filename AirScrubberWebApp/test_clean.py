import formulas
import traceback
import sys

print("Loading clean workbook...")
sys.stdout.flush()
try:
    fpath = r"Clean_Air_Scrubber.xlsx"
    xl_model = formulas.ExcelModel().loads(fpath).finish()
    
    inputs = {
        "'[Clean_Air_Scrubber.xlsx]Summary'!D1": 6000,
        "'[Clean_Air_Scrubber.xlsx]Summary'!D2": 2,
        "'[Clean_Air_Scrubber.xlsx]Summary'!D4": "Yes",
        "'[Clean_Air_Scrubber.xlsx]Summary'!D5": 1,
        "'[Clean_Air_Scrubber.xlsx]Summary'!D6": 1,
        "'[Clean_Air_Scrubber.xlsx]Summary'!D7": "PP",
        "'[Clean_Air_Scrubber.xlsx]Summary'!D8": "Vertical",
        "'[Clean_Air_Scrubber.xlsx]Summary'!D9": 2000,
        "'[Clean_Air_Scrubber.xlsx]Summary'!D10": 1000
    }
    
    outputs = [
        "'[Clean_Air_Scrubber.xlsx]Summary'!E21",
        "'[Clean_Air_Scrubber.xlsx]Summary'!G10"
    ]
    for r in range(11, 52):
        outputs.extend([
            f"'[Clean_Air_Scrubber.xlsx]Summary'!B{r}",
            f"'[Clean_Air_Scrubber.xlsx]Summary'!C{r}",
            f"'[Clean_Air_Scrubber.xlsx]Summary'!D{r}",
            f"'[Clean_Air_Scrubber.xlsx]Summary'!E{r}",
            f"'[Clean_Air_Scrubber.xlsx]Summary'!F{r}",
            f"'[Clean_Air_Scrubber.xlsx]Summary'!G{r}"
        ])
    
    print("Calculating...")
    sys.stdout.flush()
    res = xl_model.calculate(
        outputs=outputs,
        inputs=inputs
    )
    print("E21:", res.get("'[Clean_Air_Scrubber.xlsx]Summary'!E21", "NOT FOUND"))
    print("G10:", res.get("'[Clean_Air_Scrubber.xlsx]Summary'!G10", "NOT FOUND"))
    print("Row 29 Actual Dia:", res.get("'[Clean_Air_Scrubber.xlsx]Summary'!E29", "NOT FOUND"))
    sys.stdout.flush()
except Exception as e:
    print("Error:", e)
    traceback.print_exc()
