from pymongo import MongoClient

client = None
database = None

def init_connection():
  global database, client

  CONNECTION_STRING = "mongodb://admin:pass@localhost:27017/"
  if not client:
    client = MongoClient(CONNECTION_STRING)
  database = client['ai-powered-search']
  return database

def get_collection(collection_name):
  if database is None:
    init_connection()
  return database.get_collection(collection_name)