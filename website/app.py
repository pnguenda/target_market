from flask import Flask, render_template, request, send_from_directory
import cv2
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
import google_streetview.api
import time
import glob
import streetview
import itertools 


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
model.load_weights('static/model/final_model.hdf5')


COUNT = 0
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1

@app.route('/')
def man():
    return render_template('index.html')

###########upload images page###########
@app.route('/uploadImage')
def uploadImage():
    return render_template('uploadImage.html')


###########address form###########
@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        address = request.form["address"].to_numpy()
        
        np.savetxt("static/data/raw/user_address_submit.txt", address, fmt='%5s')

        #API CALL FOR USER ADDRESS SUBMIT IN FORM

        #this is the first part of the streetview, url up to the address, this url will return a 600x600px image
        #pre="https://maps.googleapis.com/maps/api/streetview?size=600x600&amp;location="
        pre="https://maps.googleapis.com/maps/api/streetview?size=600x600&location="
        
        #this is the second part of the streetview url, the text variable below, includes the path to a text file containing one address per line
        #the addresses in this text file will complete the URL needed to return a streetview image and provide the filename of each streetview image
        text="static/data/raw/sample_address_list.txt"
        
        #this is the third part of the url, needed after the address
        #this is my API key, please replace the one below with your own (google 'google streetview api key'), thanks!
        suf=f"&key={gkey}&fov=60"
        
        #this is the directory that will store the streetview images
        #this directory will be created if not present

        #**** DAVE, WHAT DIRECTORY SHOULD THIS GO? ***
        dir=r"static/data/raw/locs/"
        
        #checks if the dir variable (output path) above exists and creates it if it does not
        if not os.path.exists(dir):
            os.makedirs(dir)
        
        #opens the address list text file (from the 'text' variable defined above) in read mode ("r")
        with open(text,"r") as text_file:
        #the variable 'lines' below creates a list of each address line in the source 'text' file
        address_choice = [line.rstrip('\n') for line in open(text)]

            
        ln = address_choice[i].replace(" " , "+")

        # creates the url that will be passed to the url reader, this creates the full, valid, url that will return a google streetview image for each address in the address text file
        URL = pre+ln+suf
        #     print("URL FOR STREETVIEW IMAGE:\n"+URL)
            #creates the filename needed to save each address's streetview image locally
        filename = os.path.join(dir, "_" + str(ln)+".jpg")
        #     print("OUTPUT FILENAME:\n"+filename)
        #you can run this up to this line in the python command line to see what each step does
        #final step, fetches and saves the streetview image for each address using the url created in the previous steps
        urllib.request.urlretrieve(URL, filename)


        return redirect("/", code=302)
    return render_template("form.html")

@app.route('/prediction', methods=['POST'])
def prediction():
    global COUNT
    img = request.files['image']
    img.save(f'static/{COUNT}.jpg')    
    image = plt.imread(f'static/{COUNT}.jpg')
    resized_image = resize(image, (400,400,3))
    preds = model.predict(np.array([resized_image]))
    COUNT += 1
    return render_template('prediction.html', data=preds)

@app.route('/load_img')
def load_img():
    global COUNT
    return send_from_directory('static', f"{COUNT-1}.jpg")

if __name__ == '__main__':
    app.run(debug=True)



