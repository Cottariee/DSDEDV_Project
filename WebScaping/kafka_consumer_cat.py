from pymongo import MongoClient
from kafka import KafkaConsumer
import json
import sys
from setting import settings

# MongoDB URI
uri = settings.MONG0_URI

# MongoDB Setup
#manual change the year
try:
    client = MongoClient(uri)
    db = client["latae"]
    collection = db["category_2023"]
    print("Connected to MongoDB successfully.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    sys.exit(1)

# Kafka Consumer Setup
try:
    consumer = KafkaConsumer(
        'category_topic_2023',
        bootstrap_servers='localhost:9092',  # Replace with your Kafka broker address
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest',  # Start consuming from the latest message
        group_id='category_group',
        enable_auto_commit=True,
        session_timeout_ms=10000,
        heartbeat_interval_ms=3000,
    )
    print("Connected to Kafka successfully.")
except Exception as e:
    print(f"Error connecting to Kafka: {e}")
    sys.exit(1)

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
    try:
        for message in consumer:
            data = message.value
            insert_to_mongo(data)
    except Exception as e:
        print(f"Error during Kafka consumption: {e}")
        sys.stdout.flush()
    finally:
        consumer.close()
        print("Kafka consumer closed.")

print("Consumer running......")
consume_and_insert()
