from datetime import datetime
from elasticsearch import Elasticsearch
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["logbook_database"]  # Replace with your MongoDB database name
collection = db["daily_reports"]  # Replace with your MongoDB collection name

# Connect to Elasticsearch
es = Elasticsearch(
    ["https://localhost:9200"],
    basic_auth=("elastic", "+YiBKgNPc7Zr5S_poBg-"),
    verify_certs=False,  # Disabling SSL certificate verification (only for testing/development)
)

mapping = {
    "mappings": {
        "properties": {
            "date": {"type": "date"},
            "shift": {"type": "text"},
            "oil_side": {
                "properties": {
                    "d_01_surge_tank_drained_min": {"type": "integer"},
                    "d_02_water_tank_drained_min": {"type": "integer"},
                    "oil_readings": {"type": "text"},
                    "wc": {"type": "text"},
                    "oil_api": {"type": "text"},
                    "condy_api": {"type": "text"},
                    "comment_of_oil_side": {"type": "text"},
                }
            },
            "gas_plant": {
                "properties": {
                    "comment_of_gas_plant": {"type": "text"},
                }
            },
            "heating_station": {
                "properties": {
                    "whp": {"type": "text"},
                    "cp": {"type": "text"},
                    "wht": {"type": "text"},
                    "chock_size": {"type": "text"},
                    "flp": {"type": "text"},
                    "flt": {"type": "text"},
                    "wc_percent": {"type": "text"},
                    "casing_p": {"type": "text"},
                    "gas_closing": {"type": "text"},
                    "oil_closing": {"type": "text"},
                    "comment_of_heating_station": {"type": "text"},
                }
            },
        }
    }
}

# Create Elasticsearch index with the defined mapping
index_name = "task5"  # Replace with your desired Elasticsearch index name

# Check if the index already exists
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=mapping)

# Retrieve data from MongoDB and index into Elasticsearch
for document in collection.find():
    # Exclude _id field
    document.pop("_id", None)
    es.index(index=index_name, body=document)

print("Data indexed successfully into Elasticsearch!")
