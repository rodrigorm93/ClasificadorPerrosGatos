from flask import render_template, jsonify, Flask, redirect, url_for, request

from flask import render_template, jsonify
from app import app
import random
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image

import pandas as pd
import numpy as np
import os
from keras.models import load_model
from werkzeug import secure_filename

@app.route('/')


@app.route('/upload')
def upload_file2():
   return render_template('index.html')
@app.route('/uploaded', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['fileToUpload']
      filename = secure_filename(f.filename)
      #f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
      path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
      path2 = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
      f.save(path)

      UPLOAD_FOLDER2 = '../ClasificadorDogCat/app/static/img'

     # model= load_model("C:/Users/Rodrigo/Documents/Proyectos/ClasificadorDogCat/app/modelo/model.h5")
      model= load_model("../ClasificadorDogCat/app/modelo/model.h5")
     
      #model.load_weights ("model.h5")
      img = image.load_img(path2, target_size=(224,224))

      #imagen = '/Users/Rodrigo/Documents/flaskSaaS-master/app/static/img/' + f.filename 
      imagen= 'img/' + f.filename 

      test_df = pd.DataFrame({'filename':  [filename] })
      nb_samples = test_df.shape[0]
      #test_df = 'g1.jpg'
      IMAGE_SIZE=(128, 128)
      test_gen = ImageDataGenerator(rescale=1./255)
      test_generator = test_gen.flow_from_dataframe(test_df,UPLOAD_FOLDER2,x_col='filename', y_col=None,class_mode=None, target_size=IMAGE_SIZE,batch_size=15,shuffle=False)



      predict = model.predict_generator(test_generator, steps=np.ceil(nb_samples/15))
      
      #f.save(path)
      print(predict)
      gato = round(predict[0,0]*100,2)
      perro = round(predict[0,1]*100,2)
      return render_template('uploaded.html', title='Success', pred_cat=gato,pred_dog=perro, user_image=imagen)


@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/map')
def map():
    return render_template('map.html', title='Map')


@app.route('/map/refresh', methods=['POST'])
def map_refresh():
    points = [(random.uniform(48.8434100, 48.8634100),
               random.uniform(2.3388000, 2.3588000))
              for _ in range(random.randint(2, 9))]
    return jsonify({'points': points})


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')