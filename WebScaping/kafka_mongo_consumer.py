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

uri = settings.MONG0_URI

client = MongoClient(uri)
db = client["latae"]
collection = db["geo_la_long"]

consumer = KafkaConsumer('geo_data_topic',
                         bootstrap_servers='localhost:9092',  # change to your Kafka broker
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                         auto_offset_reset='earliest',  
                         group_id='geo_group',
                         enable_auto_commit=True
                         )  # Consumer group name


# Inserting data into MongoDB
def insert_to_mongo(data):
    try:
        collection.insert_one(data)
        print(f"Data inserted into MongoDB: {data}")
        sys.stdout.flush()
    except Exception as e:
        print(f"Error inserting data into MongoDB: {e}")
        sys.stdout.flush()

# Consume messages and insert them into MongoDB
def consume_and_insert():
    for message in consumer:
        data = message.value
        insert_to_mongo(data)

consume_and_insert()
