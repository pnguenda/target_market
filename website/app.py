from flask import Flask, render_template, \
    request, send_from_directory, redirect, jsonify
import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, BatchNormalization, Flatten
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize
#For API CALL ADDRESS SUBMIT
import urllib.request
import json
# Import google_streetview for the api module
import os
import google_streetview.api
import time
import glob
import streetview
import itertools
from config import gkey
from my_functions import address_form, image_form
from PIL import UnidentifiedImageError
import shutil
from shutil import copyfile
from datetime import datetime
import subprocess

# Image processing model

model = Sequential()

model.add(Conv2D(filters=4, kernel_size=2, padding='same',
                 activation='relu', input_shape=(400, 400, 3)))
model.add(MaxPooling2D(pool_size=2))

model.add(Conv2D(filters=8, kernel_size=2, padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.1))

model.add(Conv2D(filters=12, kernel_size=2, padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.2))

model.add(Conv2D(filters=16, kernel_size=2, padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.3))

model.add(Flatten())

model.add(Dense(256, activation='relu'))
model.add(Dropout(0.4))

model.add(Dense(3, activation='softmax'))

model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

latest_model = glob.glob('static/model/*.hdf5')[0]

print(latest_model)

model.load_weights(latest_model)


# Global variables

COUNT = 0
FORM_COUNT = 0
IS_ADDRESS = None
ln = ''

app = Flask(__name__)

app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1


# main page (index.html)

@app.route("/", methods=["GET", "POST"])
def main():

    global FORM_COUNT
    global COUNT
    global IS_ADDRESS

    if request.method == "POST":

        if "address" in request.form:

            IS_ADDRESS = True

            submit_address = request.form["address"]
            # return model predictions from user address input
            data, predictions, best_guess_category, FORM_COUNT, address = address_form(model, submit_address, FORM_COUNT)
            
            image_upload_path = f'static/images/address_submit/{FORM_COUNT-1}.jpg'

        else:

            IS_ADDRESS = False

            request_files = request.files['image']
            image_upload_path = f'static/images/upload_images/{COUNT}.jpg'
            request_files.save(image_upload_path)

            try:

                image = plt.imread(image_upload_path)

            except UnidentifiedImageError:

                #need to figure out how to redirect to current location on page
                #https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/

                return redirect('/')

            # return model_predictions from uploaded image
            data, predictions, best_guess_category, COUNT = image_form(model, image, COUNT)

        # save file in new_images. File name is determined by:
        #   category of the highest prediction percentage, followed by prediction percentage,
        #   and time stamp (year, month, day, hour, second), and if the file was from an address (API call)
        #   the address is included at the end

        current_time = f'{datetime.now().year}{datetime.now().month}{datetime.now().day}{datetime.now().hour}{datetime.now().second}'
        
        prediction = str(int(round(100*max(predictions),0)))

        code = {'Brick': '10', 'Siding': '20', 'Unknown': '00'}

        new_image_name = f'{code[best_guess_category]}_{best_guess_category}_{prediction}_{current_time}'
        
        new_image_path = f'new_images/{best_guess_category}/{new_image_name}'

        if IS_ADDRESS == True:

            address = address[0].replace(',', '').replace('.', '').replace(' ', '_')

            new_image_path = new_image_path + '_' + address

        new_image_path_with_extension = new_image_path + '.jpg'
        
        copyfile(image_upload_path, new_image_path_with_extension)

        for category in os.listdir('new_images'):

            if len(os.listdir('new_images/' + category)) >= 100:

                # for each image category

                for category in os.listdir('new_images'):
                
                # move files to corresponding directory in image database

                    for image in os.listdir('new_images/' + category):

                        shutil.move(f'new_images/{category}/{image}', f'image_database/data_for_training_06/{category.lower()}_{code[category]}')

                # run script to create new model

                subprocess.run(['python', 'create_model.py'])
                
                break
                
    else:

        data = {'Best_guess': '', 'Brick': '', 'Siding': '', 'Unknown': ''}
   
    return render_template('index.html', data=data)


###########displays image on website##########

#Note: Default image when page loads is "example.jpg" in static/images/upload_images/.
#If user uploads image onto website, uploaded image is renamed f"{COUNT-1}.jpg" and is saved to, and then retrieved from, static/images/upload_images/ and is displayed on website along with model results.
#If user types address, uploaded image is renamed f"{FORM_COUNT-1}.jpg" and is saved to, and then retrieved from, static/images/address_submit/ and is displayed on website along with model results.

@app.route('/load_image')
def load_image():
    global FORM_COUNT
    global IS_ADDRESS

    if IS_ADDRESS == True:

        return send_from_directory("static/images/address_submit/", f"{FORM_COUNT-1}.jpg")
    
    elif IS_ADDRESS == False:

        return send_from_directory("static/images/upload_images/", f"{COUNT-1}.jpg")
    
    else:

        return send_from_directory("static/images/upload_images/", "example.jpg")

if __name__ == '__main__':
    app.run(debug=True)


