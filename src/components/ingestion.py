import os
import sys
import pandas
from src import utils
from src.log import logging
from dataclasses import dataclass
from src.exception import CustomException
from sklearn.model_selection import train_test_split

@dataclass
class IngestionConfig:
    train_path:str = os.path.join('storage', 'train.csv')
    test_path:str = os.path.join('storage', 'test.csv')
    raw_path:str = os.path.join('storage', 'raw.csv')

class Ingestion:
    def __init__(self):
        self.ingestion_config = IngestionConfig()

    def start_ingestion(self):
        logging.info('Data Ingestion Begins')
        database = 'creditcard_data'
        collection = 'creditcard'
        try:
            df:pandas.DataFrame = utils.fetch_data(db_name=database, c_name=collection)
            os.makedirs(os.path.dirname(self.ingestion_config.raw_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_path, index=False, header=True)
            train, test = train_test_split(df, test_size=0.1, random_state=52)
            train.to_csv(self.ingestion_config.train_path, index=False, header=True)
            test = test.drop(columns=['default payment next month'], axis=1)
            test.to_csv(self.ingestion_config.test_path, index=False, header=True)
            return (self.ingestion_config.train_path, self.ingestion_config.test_path)
        except Exception as e:
            logging.info('Error occured while Data Ingestion')
            raise CustomException(e,sys) # type: ignore