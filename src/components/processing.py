import os
import sys
import numpy
import pandas
from src import utils
from src.log import logging
from dataclasses import dataclass
from sklearn.pipeline import Pipeline
from src.exception import CustomException
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

@dataclass
class TransformConfig:
    preprocessor_filepath:str = os.path.join('storage', 'preprocessor.dill')

class Transformation:
    def __init__(self):
        self.transform_config = TransformConfig
    
    def pipeline(self):
        try:
            logging.info('Data pipeline Initiated')
            scaler = ('Scaler', StandardScaler())
            preprocessor = Pipeline(steps=[scaler])
            logging.info('Data pipeline Completed')
            return preprocessor
        except Exception as e:
            logging.info('Error in pipeline in Data Transformation')
            raise CustomException(e,sys) # type: ignore
        
    def start_transformation(self, train_path):
        try:
            # Getting X and Y from Train and Test
            logging.info("Ingestion of data is Completed")
            train = pandas.read_csv(train_path)
            x = train.drop(columns=['default payment next month'], axis=1)
            y = train['default payment next month']
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=52)
            logging.info("Ingestion of data is Completed")

            # Scaling through pipeline
            preprocessor = self.pipeline() 
            X_train = preprocessor.fit_transform(x_train)
            X_test = preprocessor.transform(x_test)
            logging.info('scaling is completed')

            # Making of array for Train and Test
            train_arr = numpy.c_[X_train, numpy.array(y_train)]
            test_arr = numpy.c_[X_test, numpy.array(y_test)]

            utils.save_obj(filepath=self.transform_config.preprocessor_filepath, obj=preprocessor)
            logging.info('Data Transformation is completed')
            
            return (train_arr, test_arr, self.transform_config.preprocessor_filepath)
        except Exception as e:
            logging.info('Error in Data Transformation')
            raise CustomException(e,sys) # type: ignore