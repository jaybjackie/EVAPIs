from pathlib import Path
import json
import random
import string
import time
output = {"results": []}
output_file_path = Path('EV_Charging_Stations/output.json')
dc_ev_json = ["Altervim", "EA", "EleX", "etc", "MG", "PEA", "PTT"]
# dc_ev_json = ["EleX"]

# format  quanityx type: kw
# correct format
# "Type1: 11 kW,
# Type2: 7x 11 kW
# CCS2: 38 kW, CLOSED  B1" 
# 4x CCS2, 2x Type 2
# incorrect 
# 2x CCS2 (1000V 200A)
# Delta AC Mini Plus: Type 2
# 2x CCS2 (1000V 200A)
# "8 Superchargers, available 24/7, B1 floor parking lot A15-A16"
# CCS2 60 kW, CHAdeMO 60 kW, 2x CCS2 125 kW (300A)
# "2x CCS2 60 kW"
# "CCS2 90 kW, 2x CCS2 120 kW (200A)"



CHARGER_TYPES = {"CCS2", "Type1", "Type2", "CHAdeMO"}

def extract_charger_type(description: str) -> (int, list):
  """
  Extracts charger information from a description string.

  Args:
      description: The description string containing charger information.

  Returns:
      A tuple containing the total number of chargers and a list of dictionaries
      representing each charger. Each dictionary has keys 'type', 'maxChargeRateKw',
      and 'count'. If no chargers are found, returns (0, None).
  """

  chargers = []
  total_count = 0

  # Split the description by commas
  for part in description.split(','):
    # Extract charger type, count, and max charge rate
    charger_info = part.strip().split(': ')
    if len(charger_info) < 2 or len(charger_info) > 3:
      continue  # Skip invalid formats

    # Separate type and count (handle "x" multiplier in type)
    type_parts = charger_info[0].strip().split('x')
    rate_str, _ = charger_info[1:] if len(charger_info) == 3 else (charger_info[1], None)

    # Extract count (handle potential multiplier and missing value)
    try:
      count = int(type_parts[0]) if len(type_parts) == 1 else int(type_parts[0].strip())  # Attempt conversion first
    except ValueError:
      count = 1  # Default to 1 if conversion fails

    # Extract charger type (handle cases without multiplier)
    charger_type = type_parts[1] if len(type_parts) > 1 else type_parts[0].strip()

    # Extract max charge rate (handle invalid values)
    max_charge_rate = rate_str.split()[0]

    # Add charger info to dictionary and update total count
    chargers.append({"type": charger_type, "maxChargeRateKw": max_charge_rate, "count": count})
    total_count += count

  # Filter out chargers with missing information or CLOSED state
  filtered_chargers = [charger for charger in chargers if charger['maxChargeRateKw'] is not None]

  # Return total count and list of charger dictionaries (or None if empty)
  return total_count, filtered_chargers if filtered_chargers else None


def generate_custom_id():
    timestamp = str(int(time.time()))
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"ID-{timestamp}-{random_chars}"

test_cases = [
    "2x Type2: 11 kW",
    "2x CCS2: 160 kW, Type2: 11 kW",
    "4x CCS2: 150 kW, 2x Type2: 11 kW",
    "Type2: CLOSED",
    "Type1: 11 kW, 7x Type2: 11 kW, CCS2: CLOSED",
    "Type2: 22 kW, CCS2: 90 kW",
    "CCS2: 35 kW, Type2: 22 kW",
    "CCS2: 60 kW, CHAdeMO: 60 kW, 2x CCS2: 125 kW",
    "4x CCS2: null, 2x Type2: null"
]
# for case in test_cases:
#   total_count, chargers = extract_charger_type(case)
# #   print(f"Input: {case}")
#   print(f"Output: ({total_count}, {chargers})")
#   print("-" * 30)


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
                    chunk['properties']['description'] = None
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
                chunk['properties']['latitude'] = chunk['properties']['Latitude']
                del chunk['properties']['Latitude']
                chunk['properties']['longitude'] = chunk['properties']['Longitude']
                del chunk['properties']['Longitude']
                description = chunk['properties']['description']
                # print(description)
                if description != None:
                   evConnectorCount, evConnectorAggregation = extract_charger_type(description)
                #    print(f"count: {evConnectorCount}, aggregation:{evConnectorAggregation}")
                   chunk['properties']['evConnectorCount'] = evConnectorCount
                   chunk['properties']['evConnectorAggregation'] = evConnectorAggregation
                else:
                    chunk['properties']['evConnectorCount'] = None
                    chunk['properties']['evConnectorAggregation'] = None
                custom_id = generate_custom_id()
                chunk["properties"]["stationID"] = custom_id
                output["results"].append(chunk['properties'])
            

        
# Write the output to a new file
# with open(output_file_path, 'w', encoding="utf-8") as output_file:
#     json.dump(output, output_file, indent=4, ensure_ascii=False)
# print("Output file created:", output_file_path)
