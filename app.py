from flask import Flask, request, Response, render_template
from tensorflow.keras.models import load_model
import cv2
import numpy as np


# Creating a Python App running on Flask Server
app = Flask(__name__)



def predict_covid(imageToTest):
    
    model = load_model("model.h5")
    model.compile(optimizer='adam', loss="binary_crossentropy", metrics=['accuracy'])
    image = cv2.imread(imageToTest)
    image = cv2.resize(image, (64,64))
    image = np.reshape(image, [1,64,64,3])
    classes = model.predict_classes(image)
    
    label = ["Positive (Covid-19 infected)", "Negative"]
    return label[classes[0][0]]

@app.route('/')
def index():
    return render_template("image-classification-index.html")

@app.route('/upload-image', methods=['POST'])
def uploadImage():
    if request.method == 'POST': # Just to Validate if user is uploading the file in POST Request
        file = request.files['image']
        file.save(file.filename)

        label = predict_covid(file.filename)

        return render_template('image-classification-result.html', name=label)



if __name__ == '__main__':
    app.debug = True
    app.run()
    
