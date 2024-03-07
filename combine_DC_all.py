from pathlib import Path
import json
import re

def extract_charging_types(description):
    charging_types = []
    lines = description.split('\n')
    
    for line in lines:
        if "Delta AC Mini Plus" not in line:
            match = re.search(r'([A-Za-z0-9]+)\s*:\s*([^,\n]*)', line)
            if match:
                charging_type = {match.group(1): match.group(2).strip() if match.group(2).strip() else "Null"}
                charging_types.append(charging_type)
    
    return charging_types

dc_ev_json = ["Altervim", "EA", "EleX", "etc", "MG", "PEA", "PTT"]
# dc_ev_json = ["PTT"]
output = {"results": []}
output_file_path = Path('EV_Charging_Stations/output.json')

# Add up json from folder DC_EV_Charging_Station_Thailand
for ev_json in dc_ev_json:
    file_path = Path(f'DC_EV_Charging_Station_Thailand/{ev_json}.geojson')
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
        for chunk in data['features']:
            # print(chunk['properties']['description'])
            output["results"].append(chunk['properties'])

        
# Write the output to a new file
with open(output_file_path, 'w', encoding="utf-8") as output_file:
    json.dump(output, output_file, indent=4, ensure_ascii=False)
print("Output file created:", output_file_path)

# Test Cases
print(extract_charging_types("2x CCS2: 150 kW (1000V 200A), Type2: 11 kW"))
print(extract_charging_types("CCS2: 2x 50 kW\nType2: CLOSED\nParking"))
print(extract_charging_types("Type2: 22 kW\nCCS2: 2x 75 kW\nParking"))
print(extract_charging_types("Type2: 22 kW\nCCS2: CLOSED"))
print(extract_charging_types("ChargeCore NKR: 2x CCS2 (1000V 200A)"))
print(extract_charging_types("Delta AC Mini Plus: Type 2\nChargeCore NKR: 2x CCS2 (1000V 200A)"))
print(extract_charging_types("IOCharger IOCAW05C 7kW: Type 2\nIOCharger IOCAP06C 22kW: 2x Type 2\nChargeCore NKR-ADC: 2x CCS2, Type 2 (1000V 200A)"))

