import math

def get_actual_dia(d_calc):
    diameters = [25, 32, 40, 50, 65, 80, 100, 125, 150, 200, 250, 300, 350, 400]
    for d in diameters:
        if d_calc <= d: return d
    return 400

def try_float(val, default=0.0):
    try: return float(val)
    except: return default

def calculate_scrubber(inputs):
    cfm = try_float(inputs.get('cfm', 85000))
    ratio = try_float(inputs.get('ratio', 6))
    tankInside = str(inputs.get('tankInside', 'Yes'))
    workingPump = try_float(inputs.get('workingPump', 1))
    standbyPump = try_float(inputs.get('standbyPump', 1))
    material = str(inputs.get('material', 'Stainless Steel'))
    unitType = str(inputs.get('unitType', '50Coving'))
    ahuHeight = try_float(inputs.get('ahuHeight', 3850))
    ahuWidth = try_float(inputs.get('ahuWidth', 5300))

    vlookup_unit = {
        '25Box': 80, '43Step': 50, '50Step': 100, '43Coving': 86, '50Coving': 86
    }.get(unitType, 86)

    D3 = math.ceil((cfm * ratio) / 1000)
    D4 = tankInside
    D5 = workingPump
    D6 = standbyPump
    D9 = ahuHeight
    D10 = ahuWidth

    E17 = 11.5
    E18 = 1.0
    E19 = 2.0
    pi_val = 22.0 / 7.0

    # Intermediate calculations for E25, E26, G12
    x1 = math.ceil(D3 / (E17 * 0.2641))
    x2 = math.ceil(x1 / E19)
    x3 = math.ceil(math.sqrt(x2) + 1)
    
    vertical_branches = max(1, x3 - 1)
    E25 = vertical_branches * E19
    E26 = math.ceil(x2 / vertical_branches)
    
    G12 = max(168, E25 * E26)
    
    # Pipe Diameters
    D29 = math.floor(math.sqrt(((math.ceil(D3 * 0.227)) * 2) / (pi_val * 3600)) * 1000)
    E29 = get_actual_dia(D29)
    
    D30 = math.floor(math.sqrt(((math.ceil((D3 / 2) * 0.227)) * 2) / (pi_val * 3600)) * 1000)
    E30 = get_actual_dia(D30)
    
    D31 = math.floor(math.sqrt(((math.ceil(((D3 / 2) / vertical_branches) * 0.227)) * 2) / (pi_val * 3600)) * 1000)
    E31 = get_actual_dia(D31)

    E21 = math.ceil((E17 / 3.785) * G12)
    G10 = math.ceil((10.197 + 0.188 + 0.104 + 0.837 + 0.22 + 0.24 + 0.50 + 0.69) * 1.15 + (D9 / 1000))

    tables = []
    
    def add_row(sr, desc, col_d, col_e, uom, qty, is_header=False):
        if is_header:
            tables.append({"is_header": True, "desc": desc})
        else:
            tables.append({
                "is_item": True,
                "sr_no": str(sr) if sr else "",
                "desc": str(desc) if desc else "",
                "col_d": str(col_d) if col_d else "",
                "col_e": str(col_e) if col_e else "",
                "uom": str(uom) if uom else "",
                "qty": str(qty) if qty else ""
            })

    # Rows 12-20
    add_row("1", "Axial Full Cone Spray Nozzle", "Nozzle Material", "PVC", "Nos.", G12)
    add_row("", "", "Orifice Dia. (mm)", "4.8", "", "")
    add_row("", "", "Spray Angle °", "90", "", "")
    add_row("", "", "Spray Length (mm)", "460", "", "")
    add_row("", "", "End Connection BSP (M)", "3/8\"", "", "")
    add_row("", "", "Flow Rate per Nozzle (LPM)", E17, "", "")
    add_row("", "", "Inlet Pressure to Nozzle (Bar)", E18, "", "")
    add_row("", "", "Number of banks", E19, "", "")
    add_row("", "", "Number of Nozzles per bank", G12 / 2, "", "")

    # Rows 21-23
    add_row("2", "Pump", "Flow Rate per Pump (GPM)", E21, "Nos.", "-")
    add_row("", "", "Head (M)", G10, "", "")

    # Rows 25-27
    add_row("1", "Total No.of Vertical Branches (2 Banks)", "Nos.", E25, "", "")
    add_row("2", "Nozzles Qty / Vertical Branches", "Nos.", E26, "", "")

    # Rows 29-34
    G29 = math.ceil((D9 / 1000 + (D5 * 2 + D6 * 2) + 4) * 1.1)
    add_row("1", "Main Header Pipe - PN16/PN10", D29, E29, "MM", G29)
    G30 = math.ceil(D10 * 1.1 / 1000 * 2)
    add_row("2", "Sub Header Pipe - PN16/PN10", D30, E30, "MM", G30)
    if D4 == "Yes":
        G31 = math.ceil(((D9 - vlookup_unit - 150 - 400) * E19 / 1000) * 1.1)
    else:
        G31 = math.ceil(((D9 - vlookup_unit - 150) * E19 / 1000) * 1.1)
    add_row("3", "Branche Pipe - PN16/PN10", D31, E31, "MM", G31)
    add_row("4", "Drain & Overflow Pipe - PN16/PN10", 50, 50, "MM", 3)
    add_row("5", "Make-up Pipe - PN16/PN10", 25, 25, "MM", 3)
    add_row("6", "Quickfill Pipe - PN16/PN10", 50, 50, "MM", 3)

    # Rows 37-50
    add_row("1", "Flanges for Sub header Connection", E30, "Nos.", E19 * 2, "")
    add_row("2", "End Cap/Blind flange", E30, "Nos.", E19, "")
    D39 = 25 if E29 == 20 else E29
    C39 = "Ball Valve" if E29 <= 50 else "Butterfly valve (Wafer type)"
    F39 = 3 * D5 + 2 * D6
    add_row("3", C39, D39, "Nos.", F39, "")
    F40 = D5 + D6
    add_row("4", "Check valve (Wafer type)", E29, "Nos.", F40, "")
    F41 = D5 + D6
    add_row("5", "Y-type Strainer (Flanged End)", E29, "Nos.", F41, "")
    F42 = (F39 + F40 + F41) * 2
    add_row("6", "Flanges for BF, Check valve & Strainer", D39, "Nos.", F42, "")
    add_row("7", "EPDM Gasket for BF, Check valve & Strainer", D39, "Nos.", F42, "")
    add_row("8", "Ball Valve for Drain (Screwed end)", 50, "Nos.", 1 if D5 else 0, "")
    add_row("9", "Ball Valve for Quickfill (Screwed end)", 50, "Nos.", 1 if D5 else 0, "")
    add_row("10", "Float Valve", 25, "Nos.", 1 if D5 else 0, "")
    add_row("11", "Elbow", E29, "Nos.", 6 if D5 else 0, "")
    add_row("12", "Tee Joint", E29, "Nos.", D5 + D6, "")
    add_row("13", "Threaded Socket for nozzle connection", "3/8\"", "Nos.", G12, "")
    add_row("14", "Threaded End connector", E31, "Nos.", E25, "")

    return {
        "overview": {
            "gpm_calculated": E21,
            "head_g10_total": G10
        },
        "tables": tables
    }
