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
years = ['2023']

for year in years :
  file_path = f'Classifying/{year}/category.json'

  uri = settings.MONG0_URI

  client = MongoClient(uri)
  db = client["latae"]
  collection = db[f"category_{year}"]


  with open(file_path, 'r') as file:
    data = json.load(file)

  categories = []

  producer = KafkaProducer(bootstrap_servers='localhost:9092',  # change to your Kafka broker
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Sending data to Kafka
  def send_to_kafka(data):
      try:
          producer.send(f'category_topic_{year}', data)
          producer.flush()
          print("Data sent to Kafka successfully.")
      except Exception as e:
          print(f"Error sending data to Kafka: {e}")



  for record in data:
      send_to_kafka(record)
      categories.append(record)