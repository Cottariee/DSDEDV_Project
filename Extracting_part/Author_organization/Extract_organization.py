import json
import os
from glob import glob

root_folders = ['2018/', '2019/', '2020/', '2021/', '2022/', '2023/']

for root in root_folders:
    data_files = glob(os.path.join(root, '**/*'), recursive=True)

    combined_list = []
    unique_combined_list = set()

    for file_path in data_files:
        print(f"Processing file: {file_path}")
        unique_for_file = set()

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

                author_groups = (
                    data.get("abstracts-retrieval-response", {})
                    .get("item", {})
                    .get("bibrecord", {})
                    .get("head", {})
                    .get("author-group", [])
                )

                if isinstance(author_groups, dict):
                    author_groups = [author_groups]

                for author_group in author_groups:
                    if isinstance(author_group, dict):
                        affiliation = author_group.get("affiliation", {})
                        country = affiliation.get("country", None)
                        city = affiliation.get("city", None)
                        organizations = affiliation.get("organization", [])
                        if isinstance(organizations, dict):
                            organizations = [organizations]
                        for organization in organizations:
                            if isinstance(organization, dict) and "$" in organization:
                                org_name = organization["$"]
                                unique_for_file.add((country, city, org_name))
            for t in unique_for_file:
                combined_list.append(t)
                unique_combined_list.add(t)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {file_path}: {e}")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            
    organizations_list_output_file = "Extracting_part/Author_organization/" + root + "/organizations_list.json"
    unique_organizations_output_file = "Extracting_part/Author_organization/" + root + "/unique_organizations.json"

    try:
        os.makedirs(os.path.dirname(organizations_list_output_file), exist_ok=True)
        with open(organizations_list_output_file, 'w', encoding='utf-8') as f:
            json.dump(combined_list, f, indent=4)
        print(f"Organizations list saved to {organizations_list_output_file}")

        os.makedirs(os.path.dirname(unique_organizations_output_file), exist_ok=True)
        with open(unique_organizations_output_file, 'w', encoding='utf-8') as f:
            json.dump(list(unique_combined_list), f, indent=4)
        print(f"Unique organizations list saved to {unique_organizations_output_file}")
    except Exception as e:
        print(f"Error saving organizations list to file: {e}")
