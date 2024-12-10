import nltk
import json
import os
from glob import glob

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

def preprocess_text(text):
    text = text.strip().lower()
    lemmatizer = nltk.stem.WordNetLemmatizer()
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in nltk.corpus.stopwords.words('english')]
    return ' '.join(words)

root_folders = ['2018', '2019', '2020', '2021', '2022', '2023']
count1 = 0
count2 = 0
count3 = 0
count4 = 0
count5 = 0

for root in root_folders:
    data_files = glob(os.path.join(root, '**/*'), recursive=True)
    lit_info_list = []

    for json_file in data_files:
        print(f"Processing file: {json_file}")
        unique_for_file = {}
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Get source title
                source_title = (
                        data.get("abstracts-retrieval-response", {})
                        .get("item", {})
                        .get("bibrecord", {})
                        .get("head", {})
                        .get("source", {})
                        .get("sourcetitle-abbrev", str)
                    )
                if (source_title):
                    unique_for_file['sourcetitle-abbrev'] = str(source_title)
                else:
                    unique_for_file['sourcetitle-abbrev'] = ''
                    count1 += 1
                
                # Get citation title
                citation_title = (
                        data.get("abstracts-retrieval-response", {})
                        .get("item", {})
                        .get("bibrecord", {})
                        .get("head", {})
                        .get("citation-title", str)
                    )
                if (citation_title):
                    unique_for_file['citation_title'] = preprocess_text(citation_title)
                else:
                    count2 += 1
                    unique_for_file['citation_title'] = ''
                
                # Get abstracts
                abstracts = (
                        data.get("abstracts-retrieval-response", {})
                        .get("item", {})
                        .get("bibrecord", {})
                        .get("head", {})
                        .get("abstracts", str)
                    )
                if (abstracts):
                    unique_for_file['abstracts'] = preprocess_text(abstracts)
                else:
                    count3 += 1
                    unique_for_file['abstracts'] = ''
                
                # Get author keywords
                author_keywords = (
                        data.get("abstracts-retrieval-response", {})
                        .get("authkeywords",{})
                    )
                if (author_keywords):
                    author_keyword = author_keywords.get("author-keyword", [])
                    unique_auth_keyword = set()
                    for akw in author_keyword:
                        if isinstance(akw, dict) and "$" in akw:
                            unique_auth_keyword.add(akw['$'])
                        else:
                            unique_auth_keyword.add(author_keyword['$'])
                    unique_for_file['author_keywords'] = list(unique_auth_keyword)
                else:
                    count4 += 1
                    unique_for_file['author_keywords'] = ''
                
                # Get language
                language = (
                        data.get("abstracts-retrieval-response", {})
                        .get("language", {})
                    )
                if (language):
                    unique_for_file['language'] = str(language['@xml:lang'])
                else:
                    unique_for_file['language'] = ''
                    count5 += 1

                lit_info_list.append(unique_for_file)
                    
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {json_file}: {e}")
        except Exception as e:
            print(f"Error processing file {json_file}: {e}")
    print(count1, count2, count3, count4, count5)

    literature_info_output_file = "Classifying/" + root + "/literature_info.json"
    try:   
        os.makedirs(os.path.dirname(literature_info_output_file), exist_ok=True)
        with open(literature_info_output_file, 'w', encoding='utf-8') as f:
            json.dump(lit_info_list, f, indent=4)
        print(f"Already saved to {literature_info_output_file}")
    except Exception as e:
        print(f"Error saving to file: {e}")