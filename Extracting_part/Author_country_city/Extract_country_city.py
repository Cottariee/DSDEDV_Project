import json
import os
from glob import glob

root_folder = ['2018/', '2019/', '2020/', '2021/', '2022/', '2023/']

for root in root_folder:
    data_file = glob(os.path.join(root, '**/*'), recursive=True)

    cities_list = []
    unique_cities = set()

    for file_path in data_file:
        print(f"Processing file: {file_path}")
        unique_for_file = set()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

                if isinstance(data, dict):
                    author_groups = (
                        data.get("abstracts-retrieval-response", {})
                        .get("item", {})
                        .get("bibrecord", {})
                        .get("head", {})
                        .get("author-group", [])
                    )
                    if isinstance(author_groups, list):
                        for author_group in author_groups:
                            if isinstance(author_group, dict):
                                city = author_group.get("affiliation", {}).get("city", None)
                                country = author_group.get("affiliation", {}).get("country", None)
                                if city:
                                    if country:
                                        unique_for_file.add((country, city))
                elif isinstance(data, list):
                    for entry in data:
                        if isinstance(entry, dict):
                            author_groups = (
                                entry.get("abstracts-retrieval-response", {})
                                .get("item", {})
                                .get("bibrecord", {})
                                .get("head", {})
                                .get("author_groups", [])
                            )
                            if isinstance(author_groups, list):
                                for author_group in author_groups:
                                    if isinstance(author_group, dict):
                                        city = author_group.get("affiliation", {}).get("city", None)
                                        country = author_group.get("affiliation", {}).get("country", None)
                                        if city:
                                            if country:
                                                unique_for_file.add((country, city))
            for t in unique_for_file:
                cities_list.append(t)
                unique_cities.add(t)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {file_path}: {e}")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    cities_output_file = "Extracting_part/Author_country_city/" + root + '/country_cities_list.json'
    unique_cities_output_file = "Extracting_part/Author_country_city/" + root + '/unique_country_cities_list.json'
    try:
        os.makedirs(os.path.dirname(cities_output_file), exist_ok=True)
        with open(cities_output_file, 'w') as f:
            json.dump(list(cities_list), f, indent=4)
        print(f"Country_ities list saved to {cities_output_file}")
        
        os.makedirs(os.path.dirname(unique_cities_output_file), exist_ok=True)
        with open(unique_cities_output_file, 'w') as f:
            json.dump(list(unique_cities), f, indent=4)
        print(f"Unique country_ities list saved to {unique_cities_output_file}")
    except Exception as e:
        print(f"Error saving cities list to file: {e}")
