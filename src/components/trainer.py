import os
import sys
from src import utils
from src.log import logging
from dataclasses import dataclass
from src.exception import CustomException
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

@dataclass
class TrainerConfig:
    trainer_filepath:str = os.path.join('storage', 'model.dill')

class Model:
    def __init__(self, preprocessor_obj, model_obj):
        self.preprocessor_obj = preprocessor_obj
        self.model_obj = model_obj
    def predict(self, x):
        transformed_feature = self.preprocessor_obj.transform(x)
        return self.model_obj.predict(transformed_feature)
    def __repr__(self):
        return f'{type(self.model_obj).__name__}()'
    def __str__(self):
        return f'{type(self.model_obj).__name__}()'

class Trainer:
    def __init__(self):
        self.trainer_config = TrainerConfig()
    
    def start_trainer(self, train_arr, test_arr, preprocessor_path):
        try:
            logging.info('Splitting training and test datasets')
            x_train, y_train = train_arr[:,:-1], train_arr[:,-1]
            x_test, y_test = test_arr[:,:-1], test_arr[:,-1]
            model = RandomForestClassifier(n_estimators=80, max_depth=8, min_samples_split=5, min_samples_leaf=2)
            model.fit(x_train, y_train)
            logging.info('Model Training is Complete')
            logging.info('Extracting model config file path')
            preprocessor_obj = utils.load_object(filepath=preprocessor_path)
            custom_model = Model(preprocessor_obj=preprocessor_obj, model_obj=model)
            logging.info(f'Saving model at path: {self.trainer_config.trainer_filepath}')
            utils.save_obj(filepath=self.trainer_config.trainer_filepath, obj=custom_model)
            y_pred = model.predict(x_test)
            score = accuracy_score(y_test, y_pred)
            logging.info('Evaluation is Complete')
            return score
        
        except Exception as e:
            logging.info('Error in Data Training')
            raise CustomException(e,sys) # type: ignore