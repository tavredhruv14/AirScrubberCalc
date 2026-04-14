import math

def get_actual_dia(d_calc):
    diameters = [25, 32, 40, 50, 65, 80, 100, 125, 150, 200, 250, 300, 350, 400]
    for d in diameters:
        if d_calc <= d:
            return d
    return 400

def try_float(val, default=0.0):
    try:
        return float(val)
    except:
        return default

def calculate_scrubber(inputs):
    cfm         = try_float(inputs.get('cfm', 85000))
    ratio       = try_float(inputs.get('ratio', 6))
    tankInside  = str(inputs.get('tankInside', 'Yes'))
    workingPump = try_float(inputs.get('workingPump', 1))
    standbyPump = try_float(inputs.get('standbyPump', 1))
    material    = str(inputs.get('material', 'Stainless Steel'))
    unitType    = str(inputs.get('unitType', '50Coving'))
    ahuHeight   = try_float(inputs.get('ahuHeight', 3850))
    ahuWidth    = try_float(inputs.get('ahuWidth', 5300))

    vlookup_unit = {
        '25Box': 80, '43Step': 50, '50Step': 100, '43Coving': 86, '50Coving': 86
    }.get(unitType, 86)

    D3  = math.ceil((cfm * ratio) / 1000)
    D4  = tankInside
    D5  = workingPump
    D6  = standbyPump
    D9  = ahuHeight
    D10 = ahuWidth

    E17    = 11.5
    E18    = 1.0
    E19    = 2.0
    pi_val = 22.0 / 7.0

    # Nozzle layout
    x1 = math.ceil(D3 / (E17 * 0.2641))
    x2 = math.ceil(x1 / E19)
    x3 = math.ceil(math.sqrt(x2) + 1)

    vertical_branches = max(1, x3 - 1)
    E25 = vertical_branches * E19
    E26 = math.ceil(x2 / vertical_branches)
    G12 = E25 * E26

    # Pipe diameters
    D29 = math.floor(math.sqrt(((math.ceil(D3 * 0.227)) * 2) / (pi_val * 3600)) * 1000)
    E29 = get_actual_dia(D29)

    D30 = math.floor(math.sqrt(((math.ceil((D3 / 2) * 0.227)) * 2) / (pi_val * 3600)) * 1000)
    E30 = get_actual_dia(D30)

    D31 = math.floor(math.sqrt(((math.ceil(((D3 / 2) / vertical_branches) * 0.227)) * 2) / (pi_val * 3600)) * 1000)
    E31 = get_actual_dia(D31)

    # Overview metrics
    E21 = math.ceil((E17 / 3.785) * G12)
    G10 = math.ceil(
        (10.197 + 0.188 + 0.104 + 0.837 + 0.22 + 0.24 + 0.50 + 0.69) * 1.15
        + (D9 / 1000)
    )

    # TABLE 1 — Nozzle Layout
    table1 = [
        {"sr_no": "1", "item": "Total No. of Vertical Branches (2 Banks)", "uom": "Nos.", "total_qty": int(max(0, E25))},
        {"sr_no": "2", "item": "Nozzles Qty / Vertical Branch",            "uom": "Nos.", "total_qty": int(max(0, E26))},
    ]

    # TABLE 2 — Piping Schedule
    G29 = math.ceil((D9 / 1000 + (D5 * 2 + D6 * 2) + 4) * 1.1)
    G30 = math.ceil(D10 * 1.1 / 1000 * 2)
    if D4 == "Yes":
        G31 = math.ceil(((D9 - vlookup_unit - 150 - 400) * E19 / 1000) * 1.1)
    else:
        G31 = math.ceil(((D9 - vlookup_unit - 150) * E19 / 1000) * 1.1)

    table2 = [
        {"sr_no": "1", "piping_item": "Main Header Pipe - PN16/PN10",      "calculated_dia": D29, "actual_dia": E29, "total_running_mtr_qty": G29},
        {"sr_no": "2", "piping_item": "Sub Header Pipe - PN16/PN10",       "calculated_dia": D30, "actual_dia": E30, "total_running_mtr_qty": G30},
        {"sr_no": "3", "piping_item": "Branche Pipe - PN16/PN10",          "calculated_dia": D31, "actual_dia": E31, "total_running_mtr_qty": G31},
        {"sr_no": "4", "piping_item": "Drain & Overflow Pipe - PN16/PN10", "calculated_dia": 50,  "actual_dia": 50,  "total_running_mtr_qty": 3},
        {"sr_no": "5", "piping_item": "Make-up Pipe - PN16/PN10",          "calculated_dia": 25,  "actual_dia": 25,  "total_running_mtr_qty": 3},
        {"sr_no": "6", "piping_item": "Quickfill Pipe - PN16/PN10",        "calculated_dia": 50,  "actual_dia": 50,  "total_running_mtr_qty": 3},
    ]

    # TABLE 3 — Accessories & Valves
    D39 = 25 if E29 == 20 else E29
    C39 = "Ball Valve" if E29 <= 50 else "Butterfly valve (Wafer type)"
    F39 = int(3 * D5 + 2 * D6)
    F40 = int(D5 + D6)
    F41 = int(D5 + D6)
    F42 = int((F39 + F40 + F41) * 2)

    table3 = [
        {"sr_no": "1",  "accessories_item": "Flanges for Sub header Connection",           "actual_size": E30,    "total_qty": int(E19 * 2)},
        {"sr_no": "2",  "accessories_item": "End Cap / Blind flange",                      "actual_size": E30,    "total_qty": int(E19)},
        {"sr_no": "3",  "accessories_item": C39,                                            "actual_size": D39,    "total_qty": F39},
        {"sr_no": "4",  "accessories_item": "Check valve (Wafer type)",                    "actual_size": E29,    "total_qty": F40},
        {"sr_no": "5",  "accessories_item": "Y-type Strainer (Flanged End)",                "actual_size": E29,    "total_qty": F41},
        {"sr_no": "6",  "accessories_item": "Flanges for BF, Check valve & Strainer",      "actual_size": D39,    "total_qty": F42},
        {"sr_no": "7",  "accessories_item": "EPDM Gasket for BF, Check valve & Strainer",  "actual_size": D39,    "total_qty": F42},
        {"sr_no": "8",  "accessories_item": "Ball Valve for Drain (Screwed end)",           "actual_size": 50,     "total_qty": 1 if D5 else 0},
        {"sr_no": "9",  "accessories_item": "Ball Valve for Quickfill (Screwed end)",       "actual_size": 50,     "total_qty": 1 if D5 else 0},
        {"sr_no": "10", "accessories_item": "Float Valve",                                  "actual_size": 25,     "total_qty": 1 if D5 else 0},
        {"sr_no": "11", "accessories_item": "Elbow",                                        "actual_size": E29,    "total_qty": 6 if D5 else 0},
        {"sr_no": "12", "accessories_item": "Tee Joint",                                    "actual_size": E29,    "total_qty": int(D5 + D6)},
        {"sr_no": "13", "accessories_item": "Threaded Socket for nozzle connection",        "actual_size": '1/2"', "total_qty": int(G12)},
        {"sr_no": "14", "accessories_item": "Threaded End connector",                       "actual_size": E31,    "total_qty": int(E25)},
    ]

    return {
        "overview": {
            "gpm_calculated":        E21,
            "head_g10_total":        G10,
            "total_nozzles":         int(G12),
            "vertical_branches":     int(E25),
            "nozzles_per_bank":      int(G12 / 2),
            "flow_lpm_per_nozzle":   E17,
            "inlet_pressure_bar":    E18,
            "num_banks":             int(E19),
        },
        "table1": table1,
        "table2": table2,
        "table3": table3,
    }
