import pandas as pd
from pymongo.mongo_client import MongoClient

uri = 'mongodb+srv://Piyush:cUxjKK4nwQVaHuK4@cluster0.opvarp6.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(uri)
database = 'creditcard_data'
collection = 'creditcard'
df = pd.read_csv(r'C:\Users\p12m9\Documents\Python Coding\PW\Projects\P3)_CreditCardFraudDetection\notebook\ccFraud.csv')
ds = df.to_dict(orient='records')
client[database][collection].insert_many(ds)