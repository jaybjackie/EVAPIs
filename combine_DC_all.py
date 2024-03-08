from pathlib import Path
import json
import re

output = {"results": []}
output_file_path = Path('EV_Charging_Stations/output.json')
dc_ev_json = ["Altervim", "EA", "EleX", "etc", "MG", "PEA", "PTT"]
# dc_ev_json = ["EleX"]


def extract_charger_type(description: str):
    # TODO Extract Charger from each provider
    # Altervim: "2x CCS2: 160 kW, Type2: 11 kW" & "4x CCS2: 150 kW (1000V 200A), 2x Type2: 11 kW" /
    # EA: "CCS2: 118 kW, 200A, Type2: CLOSED" & /
    # "Type1: 11 kW, Type2: 7x 11 kW, CCS2: 38 kW, CLOSED  B1" & /
    # "CCS2: 35 kW, Type2: 22 kW" & /
    # "Type2: 22 kW, CCS2: 2x 150 kW, 200A  ครัวในซอย" &/
    # "Type2: 22 kW, CCS2: 2x 110 kW, 200A  SCB"/
    # "Type2: 22 kW, CCS2: 90 kW, 200A" /
    # EleX: "2x CCS2 60 kW" & "CCS2 90 kW, 2x CCS2 120 kW (200A)"/
    # "CCS2 60 kW, CHAdeMO 60 kW, 2x CCS2 125 kW (300A)"
    # etc -> Sharge
    # "2x CCS2: 60 kW, Type2: 22 kW"
    # Tesla -> "8 Superchargers, available 24/7, B1 floor parking lot A15-A16" กำลังไฟ 250 kW หาcharger type
    # MEA -> "4x CCS2, 2x Type 2" &  "CCS2, CHAdeMO, Type 2" & "3x CCS2, CHAdeMO, 5x Type 2"
    # EVolt -> "2x CCS2" & null
    # Galvanic -> "CCS2: 15 kW, Type2: 7 kW" & "2x CCS2: 120 kW"
    # MG, PEA-> ไม่มี charger type มีแต่ power
    # PTT -> "CCSx2: 2x CCS2 (1000V 200A)" & "2x CCS2 (1000V 200A)"
    # "Delta AC Mini Plus: Type 2, 2x CCS2 (1000V 200A)"
    # " 22kW: 2x Type 2, CCSx2: 2x CCS2 (1000V 200A), CCSx2: 2x CCS2 (1000V 200A)"


# {"type": "", "maxChargeRateKw": 0, "count": 0}
# extract_charger_type("Type2: 11 kW") output: (1 ,[{"type": "Type2", "maxChargeRateKw": 11, "count": 1}])
# extract_charger_type("2x CCS2: 160 kW, Type2: 11 kW") output: (3, [{"type": "CCS2", "maxChargeRateKw": 160, "count": 2}, {"type": "Type2", "maxChargeRateKw": 11, "count": 1}])
# extract_charger_type("4x CCS2: 150 kW (1000V 200A), 2x Type2: 11 kW") output: (6, [{"type": "CCS2", "maxChargeRateKw": 150 kW, "count": 4}, {"type": "Type2", "maxChargeRateKw": 11, "count": 2}])
# extract_charger_type("CCS2: 118 kW, 200A, Type2: CLOSED") output: (1, [{"type": "CCS2", "maxChargeRateKw": 118, "count": 1}])
# extract_charger_type("Type1: 11 kW, Type2: 7x 11 kW, CCS2: 38 kW, CLOSED  B1") output: (9, [{"type": "Type1", "maxChargeRateKw": 1, "count": 1}, {"type": "Type2", "maxChargeRateKw": 11, "count": 7}, {"type": "CCS2", "maxChargeRateKw": 28, "count": 1}])
# extract_charger_type("CCS2: 35 kW, Type2: 22 kW") output: (2, [{"type": "CCS2", "maxChargeRateKw": 35, "count": 1}, {"type": "Type2", "maxChargeRateKw": 22, "count": 1}])
# extract_charger_type("Type2: 22 kW, CCS2: 2x 150 kW, 200A  ครัวในซอย") output: (3, [{"type": "Type2", "maxChargeRateKw": 22, "count": 1}, {"type": "CCS2", "maxChargeRateKw": 150, "count": 2}])
# extract_charger_type("Type2: 22 kW, CCS2: 2x 110 kW, 200A  SCB") output: (3, [{"type": "Type2", "maxChargeRateKw": 22, "count": 1}, {"type": "CCS2", "maxChargeRateKw": 150, "count": 2}])
# extract_charger_type("Type2: 22 kW, CCS2: 90 kW, 200A") output: (2, [{"type": "Type2", "maxChargeRateKw": 22, "count": 1}, {"type": "CCS2", "maxChargeRateKw": 90, "count": 1}])
# extract_charger_type("2x CCS2 60 kW" & "CCS2 90 kW, 2x CCS2 120 kW (200A)") output: (5, [{"type": "CCS2", "maxChargeRateKw": 60, "count": 2}, {"type": "CCS2", "maxChargeRateKw": 90, "count": 1}, {"type": CCS2 "maxChargeRateKw": 120, "count": 2}])
# extract_charger_type("CCS2 60 kW, CHAdeMO 60 kW, 2x CCS2 125 kW (300A)") output: (4, [{"type": "CCS2", "maxChargeRateKw": 60, "count": 1}, {"type": "CHAdeMO", "maxChargeRateKw": 60, "count": 1}, {"type": "CCS2", "maxChargeRateKw": 125, "count": 2}])
    
    print("nothing")

# Add up json from folder DC_EV_Charging_Station_Thailand
for ev_json in dc_ev_json:
    file_path = Path(f'DC_EV_Charging_Station_Thailand/{ev_json}.geojson')
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
        for chunk in data['features']:
            if chunk['properties']['Power'] != None and\
                chunk['properties']['Power'] != "0 kW":
                if chunk['properties']['Provider'] == "EA":
                    if chunk['properties']['Hours'] != "0 kW":
                        del chunk['properties']['Hours']
                        output["results"].append(chunk['properties'])
                if chunk['properties']['Provider'] == "PTT":
                    del chunk['properties']['Name_EN']
                if chunk['properties']['Provider'] == "PEA":
                    chunk['properties']['Address'] = chunk['properties']['description']
                    chunk['properties']['escription'] = None
                    chunk['properties']['evConnectorCount'] = None
                    chunk['properties']['evConnectorAggregation'] = None
                if chunk['properties']['Provider'] == "MG":
                    chunk['properties']['description'] = chunk['properties']['Dealership']
                    del chunk['properties']['Dealership']
                    chunk['properties']['evConnectorCount'] = None
                    chunk['properties']['evConnectorAggregation'] = None
                # if chunk['properties']['Provider'] == "EleX":
                #     continue
                chunk['properties']['name'] = chunk['properties']['Name']
                del chunk['properties']['Name']
                chunk['properties']['power'] = chunk['properties']['Power']
                del chunk['properties']['Power']
                chunk['properties']['address'] = chunk['properties']['Address']
                del chunk['properties']['Address']
                chunk['properties']['provider'] = chunk['properties']['Provider']
                del chunk['properties']['Provider']
                
                output["results"].append(chunk['properties'])
            

        
# Write the output to a new file
with open(output_file_path, 'w', encoding="utf-8") as output_file:
    json.dump(output, output_file, indent=4, ensure_ascii=False)
print("Output file created:", output_file_path)

