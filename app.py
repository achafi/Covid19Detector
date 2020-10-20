from flask import Flask, request,redirect, Response, render_template, flash, session
from tensorflow.keras.models import load_model
import cv2
import os
import numpy as np
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message



# Creating a Python App running on Flask Server
app = Flask("covid_detector")
PEOPLE_FOLDER = "C:/Users/post/Desktop/ML_projects/COVID-19 X-RayCNN/Covid19Detector/static/xrayimage"
ALLOWED_IMAGE_EXTENSIONS = ["JPG", "PNG", "JPEG"]
app.secret_key = "dont tell anyone"
app.config.from_pyfile('config.cfg')

app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
app.config['ALLOWED_IMAGE_EXTENSIONS'] = ALLOWED_IMAGE_EXTENSIONS



mail = Mail(app)


def predict_covid(imageToTest):
    """
        Takes in an image and returns label : "Positive (Covid-19 infected)" or "Negative"
    """
    
    model = load_model("model_files/model.h5")
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
            
            # Errors Handling
            if file.filename == "":
                
                flash("Image must have filename !", 'error')
                return redirect("/")
            
            elif not allowed_image(file.filename) :
                flash("The image extension is not allowed !", 'error')
                return redirect("/")
            
            else :
                
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
                # save image for further use
                file.save(path)
        
                # predict the image class
                label = predict_covid(path)
                return render_template('image-classification-result.html', user_image = filename, name=label)
    

"""   
# Send Email via send message button
@app.route('/send_message', methods=['POST', 'GET'])
def send_message():
    if request.method == "POST":
        name = request.form['Name']
        Email = request.form['Email']
        message = name + "\n" + Email +"\n"+ request.form['Message']
        #msg = Message(message, sender=['assia.chafii93@gmail.com'], recipients=['assia.chafii93@gmail.com'])
        msg = Message('Hello', sender = 'assia.chafii93@gmail.com', recipients = ['assia.chafii93@gmail.com'])
        msg.body = message
        mail.send(msg)
        flash('Message sent! Thank you :)', 'info')
        return redirect("/")
        
    return redirect("/")
"""


if __name__ == '__main__':


    app.debug = True
    app.run()
    
