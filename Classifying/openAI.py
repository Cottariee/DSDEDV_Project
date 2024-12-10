import openai
import json
from glob import glob
import os
from setting import settings

# Replace with your OpenAI API key
openai.api_key = settings.OPENAI_API_KEY
openai.organization = settings.OPENAI_ORGANIZATION

def categorize_text(data):
    categorized_data = []
    data_categories = "\nData Category:\n1. Renewable Energy\n2. Environmental Science\n3. Medical Research\n4. Computational Technologies\n5. Materials Science\n6. Chemical Engineering\n7. Physics\n8. Education and Social Sciences\n9. Biotechnology, Bioengineering and Life Sciences\n10. Agriculture and Food Science\n11. Health and Wellness\n12. Environmental Policy and Governance\n13. Nanotechnology\n14. Ecology and Conservation\n15. Food Science"
    for entry in data:
        citation_title = entry["citation_title"]
        abstracts = entry["abstracts"]
        if (isinstance(entry["author_keywords"], list)):
            author_keywords = ', '.join(entry["author_keywords"])
        else:
            author_keywords = entry["author_keywords"]
        text = f"Instructions:\n1.Given the following categories list, categorize each piece of data accordingly: {data_categories}\n2.Categorize the data delimited in angle brackets the most appropriate categories from the list above by analysis citation, abstracts, and author keywords of each data. A piece of news can be assigned to more than one category if applicable. Output just a list of the category. No describe needed.\n\nThe data:\n<Title: {citation_title}\nAbstract: {abstracts}\nKeywords: {author_keywords}>"
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert in categorizing academic research papers."},
                {"role": "user", "content": text}],
            max_tokens=2000
        )
        category = response['choices'][0]['message']['content'].split("\n")
        categorized_data.append({"sourcetitle-abbrev": entry['sourcetitle-abbrev'], "citation_title": entry['citation_title'], "category": category, "abstracts": entry['abstracts'], "keywords": entry['author_keywords'], "language": entry['language']})
    return categorized_data

root_folder = ['2018/', '2019/', '2020/', '2021/', '2022/', '2023/']

for root in root_folder:
    data_file = f'Classifying/{root}literature_info.json'
    categories = []
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            categories = categorize_text(data)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file {data_file}: {e}")
    except Exception as e:
        print(f"Error processing file {data_file}: {e}")
    
    category_list_output_file = f"Classifying/{root}category.json"
    try:
        os.makedirs(os.path.dirname(category_list_output_file), exist_ok=True)
        with open(category_list_output_file, 'w', encoding='utf-8') as f:
            json.dump(categories, f, indent=4)
        print(f"Already saved to {category_list_output_file}")
    except Exception as e:
        print(f"Error saving to file: {e}")

