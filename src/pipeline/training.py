import os
import sys
import pandas as pd
from src.log import logging
from src.exception import CustomException
from src.components.ingestion import Ingestion
from src.components.processing import Transformation
from src.components.trainer import Trainer

class TrainingPipeline:
    def __init__(self)->None:
        self.ingection = Ingestion()
        self.transformation = Transformation()
        self.trainer = Trainer()

    def start_pipeline(self):
        try:
            train_path, _ = self.ingection.start_ingestion()
            (train, test, preprocessor_filepath) = self.transformation.start_transformation(train_path=train_path)
            score = self.trainer.start_trainer(train_arr=train, test_arr=test, preprocessor_path=preprocessor_filepath,)
            print('Training Completed\nTrained model score: ', score)
        except Exception as e:
            logging.info('Error in training pipeline')
            raise CustomException(e,sys) # type: ignore