from pymongo import MongoClient
from kafka import KafkaConsumer, KafkaProducer
import json
import time
import threading 
from bs4 import BeautifulSoup                                                                                       
import requests
import ast
import pandas as pd
import io
import sys
from setting import settings

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
file_path = 'Extracting_part/Author_country_city/Unique_country_city/global_unique_country_cities.json'
uri = settings.MONG0_URI

client = MongoClient(uri)
db = client["latae"]
collection = db["global_unique_cities"]


with open(file_path, 'r') as file:
  data = json.load(file)

producer = KafkaProducer(bootstrap_servers='localhost:9092',  # change to your Kafka broker
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Sending data to Kafka
def send_to_kafka(data):
    try:
        producer.send('geo_data_topic', data)
        producer.flush()
        print("Data sent to Kafka successfully.")
    except Exception as e:
        print(f"Error sending data to Kafka: {e}")



locations = data
coordinates = []

# Function to convert DMS to Decimal Degrees
def dms_to_decimal(dms):
    direction = dms[0]  
    dms_cleaned = dms[1:].strip()  
    dms_cleaned = dms_cleaned.replace("°", " ").replace("′", " ").replace("″", " ").replace("'", " ")
    parts = dms_cleaned.split()  
    degrees = float(parts[0])
    minutes = float(parts[1]) if len(parts) > 1 else 0
    seconds = float(parts[2]) if len(parts) > 2 else 0
    decimal = degrees + (minutes / 60) + (seconds / 3600)
    if direction in ['S', 'W']:
        decimal = -decimal
    return round(decimal, 4)

def no_data(country, city):
    data2 = {
                            "Country": country,
                            "City": city,
                            "Latitude": 'No Data',
                            "Longitude": 'No Data'
                        }
    send_to_kafka(data2)
    print(data2)
    sys.stdout.flush

for city in locations:
    search_query = city[1]
    expected_country = city[0]
    url = f"https://www.geonames.org/search.html?q={search_query}&country="

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the table containing the latitude and longitude
        table = soup.find("table", class_="restable")
        
        # Check if the table exists
        if table:
            rows = table.find_all("tr")
            df_added = False
            # Process the first result
            for row in rows:
                cells = row.find_all("td")
                if len(cells) >= 6:  # Check there are enough columns
                    lat_dms = cells[4].text.strip()  # Latitude in DMS format
                    lon_dms = cells[5].text.strip()  # Longitude in DMS format
                    country = cells[2].text.strip()
                    if (expected_country.lower() in country.lower()):
                        try:
                            lat_decimal = dms_to_decimal(lat_dms)
                            lon_decimal = dms_to_decimal(lon_dms)
                            data2 = {
                            "Country": city[0],
                            "City": city[1],
                            "Latitude": lat_decimal,
                            "Longitude": lon_decimal
                            }
                            send_to_kafka(data2)
                            print(data2)
                            sys.stdout.flush()
                            # print('gooddd')
                            df_added = True
                        except ValueError as e:
                            print(f"Error converting DMS for {city}: {e}")
                        break
                    else:
                        no_data(city[0], city[1])
                        # print('not match')
                        df_added = True
                        break
            if not df_added:
                no_data(city[0], city[1])
        else:
            no_data(city[0], city[1])
            # print('not found')
    else:
        print(f"Failed to fetch data for {search_query}, Status code: {response.status_code}")
        no_data(city[0], city[1])
        


df = pd.DataFrame(coordinates)