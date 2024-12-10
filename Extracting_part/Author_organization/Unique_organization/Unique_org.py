import json
import os
from glob import glob

json_folder = "Extracting_part/Author_organization/"
global_unique_combined_list = set()
json_files = glob(os.path.join(json_folder, '*/*.json'))

for json_file in json_files:
    print(f"Processing file: {json_file}")
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, list) and len(item) == 3:
                        global_unique_combined_list.add(tuple(item))
                    else:
                        print(f"Skipping invalid item in {json_file}: {item}")
            else:
                print(f"Skipping non-list data in {json_file}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file {json_file}: {e}")
    except Exception as e:
        print(f"Error processing file {json_file}: {e}")
        
print(len(global_unique_combined_list))
output_file = "Extracting_part/Author_organization/Unique_organization/global_unique_organizations.json"
try:
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(list(global_unique_combined_list), f, indent=4)
    print(f"Global unique organizations list saved to {output_file}")
except Exception as e:
    print(f"Error saving global organizations list to file: {e}")