import os
import sys
import dill
import numpy
import pandas
from src.log import logging
from pymongo import MongoClient
from src.exception import CustomException

def fetch_data(db_name, c_name):
    try:
        uri = 'mongodb+srv://Piyush:cUxjKK4nwQVaHuK4@cluster0.opvarp6.mongodb.net/?retryWrites=true&w=majority'
        client = MongoClient(uri)
        collection = client[db_name][c_name]
        df = pandas.DataFrame(list(collection.find()))
        if '_id' in df.columns.to_list():
            df = df.drop(columns=['_id'], axis=1)
        df.replace({'na':numpy.nan}, inplace=True)
        return df
    
    except Exception as e:
        logging.info('Error in collecting file from mongoDB')
        raise CustomException(e,sys) # type: ignore

def save_obj(filepath, obj):
    try:
        dir_path = os.path.dirname(filepath)
        os.makedirs(dir_path, exist_ok=True)
        with open(filepath, 'wb') as file_obj:
            dill.dump(obj, file_obj)
            
    except Exception as e:
        logging.info('Error in saving dill file')
        raise CustomException(e,sys) # type: ignore

def load_object(filepath):
    try:
        with open(filepath,'rb') as file_obj:
            logging.info('Loading object from utils is completed')
            return dill.load(file_obj)
        
    except Exception as e:
        logging.info('Error occured while loading object from utils')
        raise CustomException(e,sys) # type: ignore