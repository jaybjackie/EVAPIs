import json
from pathlib import Path

dc_ev_json = ["Altervim", "EA", "EleX", "etc", "MG", "PEA", "PTT"]

# Add up json from folder DC_EV_Charging_Station_Thailand
for ev_json in dc_ev_json:
    file_path = Path(f'DC_EV_Charging_Station_Thailand/{ev_json}.geojson')
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
        output = {"providers": f'{ev_json}', "results": []}
        output_file_path = Path(f'EV_Charging_Stations/{ev_json}_output.json')
        for chunk in data['features']:
            output["results"].append(chunk['properties'])
    # Write the output to a new file
    with open(output_file_path, 'w', encoding="utf-8") as output_file:
        json.dump(output, output_file, indent=4, ensure_ascii=False)
        print("Output file created:", output_file_path)

        
