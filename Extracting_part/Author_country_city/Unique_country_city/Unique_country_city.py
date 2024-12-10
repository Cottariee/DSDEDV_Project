import json
import os
from glob import glob

input_folder = "Extracting_part/Author_country_city/"
global_unique_cities = set()
json_files = glob(os.path.join(input_folder, '**/*.json'), recursive=True)

for json_file in json_files:
    print(f"Processing file: {json_file}")
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, list) and len(item) == 2:
                        global_unique_cities.add(tuple(item))
                    else:
                        print(f"Skipping invalid item in {json_file}: {item}")
            else:
                print(f"Skipping non-list data in {json_file}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file {json_file}: {e}")
    except Exception as e:
        print(f"Error processing file {json_file}: {e}")

print(len(global_unique_cities))
output_file = "Extracting_part/Author_country_city/Unique_country_city/global_unique_country_cities.json"
try:
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump([list(city) for city in global_unique_cities], f, indent=4)
    print(f"Global unique country-city list saved to {output_file}")
except Exception as e:
    print(f"Error saving global country-city list to file: {e}")
