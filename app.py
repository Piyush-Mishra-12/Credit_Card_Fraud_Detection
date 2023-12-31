from flask import Flask, render_template, jsonify, request, send_file
from src.exception import CustomException
from src.log import logging
import os, sys

from src.pipeline.training import TrainingPipeline
from src.pipeline.prediction import Prediction

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to my App"

@app.route("/train")
def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.start_pipeline()
        return "Training Completed."
    except Exception as e:
        raise CustomException(e,sys) # type: ignore

@app.route('/predict', methods=['POST', 'GET'])
def upload():
    try:
        if request.method == 'POST':
            prediction_pipeline = Prediction(request)
            prediction_file_detail = prediction_pipeline.run_pipe()
            logging.info("prediction completed. Downloading prediction file.")
            return send_file(prediction_file_detail,
                            download_name= prediction_pipeline.PredictFilename,
                            as_attachment= True)
        else:
            return render_template('upload_file.html')
    except Exception as e:
        raise CustomException(e,sys) # type: ignore

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8089)
