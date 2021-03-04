from __future__ import division, print_function
import sys
import os
import glob
import re
import numpy as np
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__,template_folder='templates')
MODEL_PATH = 'model.h5'
model = load_model(MODEL_PATH)

def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(244, 244))

   
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    preds = model.predict(x)
    preds = np.argmax(preds,axis=1)
    return preds


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        preds = model_predict(file_path, model)   # ImageNet Decode
        class_names =  ["COVID-19","NORMAL","Viral Pneumonia"]
        output = class_names[preds[0]]
        print(output)
        return render_template('index.html', prediction='{}'.format(output))


if __name__ == '__main__':
    app.run(debug=True)
