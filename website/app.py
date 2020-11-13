from flask import Flask, render_template, request, send_from_directory
import cv2
import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, BatchNormalization, Flatten
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize

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
        address = request.form["address"]
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



