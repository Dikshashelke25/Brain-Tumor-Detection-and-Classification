from __future__ import division, print_function
import sys
import os
import glob
import re
import numpy as np

# Keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH ='newbraintumormodel.h5'

# Load your trained model
model = load_model(MODEL_PATH)




def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    ## Scaling
    x = x/255
    print(x)
    x = np.expand_dims(x, axis=0)
    print(x)
    preds = np.argmax(model.predict(x), axis=1)
    
    if preds == 0:
        preds = "The MRI contains glioma tumor"
    elif preds == 1:
        preds = "Invalid Image"
    elif preds == 2:
        preds = "The MRI contains meningioma tumor"
    elif preds == 3:
        preds = "The MRI contains no tumor"
    else:
        preds = "The MRI contains pituitary tumor"
        
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        result= preds
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)
