from flask import Flask, request,redirect, Response, render_template
from tensorflow.keras.models import load_model
import cv2
import os
import numpy as np
from werkzeug.utils import secure_filename



PEOPLE_FOLDER = "C:/Users/post/Desktop/ML_projects/COVID-19 X-RayCNN/Covid19Detector/static/xrayimage"
ALLOWED_IMAGE_EXTENSIONS = ["JPG", "PNG", "JPEG"]
# Creating a Python App running on Flask Server
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
app.config['ALLOWED_IMAGE_EXTENSIONS'] = ALLOWED_IMAGE_EXTENSIONS



def predict_covid(imageToTest):
    """
    """
    
    model = load_model("model.h5")
    model.compile(optimizer='adam', loss="binary_crossentropy", metrics=['accuracy'])
    image = cv2.imread(imageToTest)
    image = cv2.resize(image, (64,64))
    image = np.reshape(image, [1,64,64,3])
    classes = model.predict_classes(image)
    
    label = ["Positive (Covid-19 infected)", "Negative"]
    return label[classes[0][0]]

# route to home page
@app.route('/')
def index():
    return render_template("home.html")

def allowed_image(filename):
    """
        - Check file name if it is allowded 
    """
    if not "." in filename :
        return False
    ext = filename.split(".", 1)[1]
    print(ext)
    if ext.upper() in app.config['ALLOWED_IMAGE_EXTENSIONS']:
        return True
    else:
        return False
    

# route to upload image
@app.route('/upload-image', methods=['GET','POST'])
def uploadImage():
    if request.method == 'POST': # Just to Validate if user is uploading the file in POST Request
        if request.files:
            file = request.files['image']
            
            print(file.filename)
            
            # Errors Handling
            if file.filename == "":
                Error = "Image must have filename !"
                return render_template("home.html", error = Error)
            
            elif not allowed_image(file.filename) :
                Error = "The image extension is not allowed !"
                return render_template('home.html', error = Error)
            
            else:
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
                # save image for further use
                file.save(path)
        
                # predict the image class
                label = predict_covid(path)
                return render_template('image-classification-result.html', user_image = filename, name=label)

    return redirect("/")            
        


if __name__ == '__main__':
    app.debug = True
    app.run()
    
