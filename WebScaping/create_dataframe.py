import pandas as pd
from pymongo import MongoClient
import sys
import io
import re
from setting import settings

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
# MongoDB URI and client connection
uri = settings.MONG0_URI
client = MongoClient(uri)

# Connect to the database and collection
db = client["latae"]
collection_global_unique_cities = db["global_unique_cities"] 
years = ['2018', '2019', '2020', '2021', '2022' , '2023']
for year in years :
  collection_category_ = db[f'category_{year}']
  

# Fetch all data from MongoDB
  data_unique_cities = list(collection_global_unique_cities.find({}))  # Converts the cursor into a list
  data_category_ = list(collection_category_.find({})) 

# Convert the list of documents to a pandas DataFrame
  df = pd.DataFrame(data_unique_cities)
  df = df.drop(columns=['_id'])
  df = df.drop_duplicates()
  df = df[df['Country'] != 'T']
  df_cleaned = df[(df['Latitude'] != 'No Data') & (df['Longitude'] != 'No Data') ]

  for document in data_category_:
      document.pop('_id', None)

  category_year = []
  pattern = r'[.\d\s]'  

  for e in data_category_ :
     data = {
        'sourcetitle-abbrev' : e['sourcetitle-abbrev'],
        'citation_title' : e['citation_title'] ,
        'language' : e['language'] ,
        }
     citation_title = e['citation_title']
     citation_words = citation_title.split()
    
     if len(citation_words) > 100:
         data['citation_title'] = ' '.join(citation_words[:100]) + '...' 
     for each_category in e['category'] :
         data_copy = data.copy()
         each_category_cleaned = re.sub(pattern, '', each_category)
         data_copy['category'] = each_category_cleaned
         category_year.append(data_copy)

  df_category_ = pd.DataFrame(category_year)
  df_category_['year'] = year
  df_category_.to_csv(f'category_{year}.csv' , index=False)
  print(df_category_)

df.to_csv('DataVisualization/original_city.csv' , index=False)
df_cleaned.to_csv('DataVisualization/cleaned_city.csv', index=False)