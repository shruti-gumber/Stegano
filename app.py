from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import cv2
import numpy as np
import random
import time
from stegano import lsb
import os
import pyrebase
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static\\uploads\\'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




config={
    "apiKey": "AIzaSyBUiToMpgyJYI3EUZ0U4cr3VS-zMzTccfE",
    "authDomain": "python-83560.firebaseapp.com",
    "databaseURL": "https://python-83560-default-rtdb.firebaseio.com",
    "projectId": "python-83560",
    "storageBucket": "python-83560.appspot.com",
    "messagingSenderId": "439817628919",
    "appId": "1:439817628919:web:9fa080fd41b8cf052bf7f2"

}


firebase=pyrebase.pyrebase.initialize_app(config)
auth=firebase.auth()
@app.route('/')
@app.route("/index")
def new():
    return render_template("index.html")

@app.route("/image_hiding")
def test_for_image():
    return render_template("image_hiding.html")
@app.route("/image_hiding",methods=['GET','POST'])
def the_final_for_image_hiding():
    if request.method == 'POST':
        try:
            file = request.files['file']
            file2=request.files['file1']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if file2 and allowed_file(file2.filename):
                filename2=secure_filename(file2.filename)
                file2.save(os.path.join(app.config['UPLOAD_FOLDER'],filename2))
            # img1 and img2 are the
            # two input images
            img1 = cv2.imread("./static/uploads/"+secure_filename(file.filename))
            img2 = cv2.imread("./static/uploads/"+secure_filename(file2.filename))

            for i in range(img2.shape[0]):
                for j in range(img2.shape[1]):
                    for l in range(3):
                        # v1 and v2 are 8-bit pixel values
                        # of img1 and img2 respectively
                        v1 = format(img1[i][j][l], '08b')
                        v2 = format(img2[i][j][l], '08b')

                        # Taking 4 MSBs of each image
                        v3 = v1[:4] + v2[:4]

                        img1[i][j][l] = int(v3, 2)

            cv2.imwrite('./static/uploads/encrypt.png', img1)
            return render_template("image_hiding.html",umessage="yes")
        except:
                return render_template("image_hiding.html")
    else:
        return render_template("image_hiding.html")

@app.route("/image_showing")
def image_showing():
    return render_template("/image_showing.html")
@app.route("/image_showing", methods=['GET','POST'])
def image_to_be_showed():
    if request.method == 'POST':
        try:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            img = cv2.imread('.static/uploads/'+filename)
            width = img.shape[0]
            height = img.shape[1]

            # img1 and img2 are two blank images
            img1 = np.zeros((width, height, 3), np.uint8)
            img2 = np.zeros((width, height, 3), np.uint8)

            for i in range(width):
                for j in range(height):
                    for l in range(3):
                        v1 = format(img[i][j][l], '08b')
                        v2 = v1[:4] + chr(random.randint(0, 1) + 48) * 4
                        v3 = v1[4:] + chr(random.randint(0, 1) + 48) * 4

                        # Appending data to img1 and img2
                        img1[i][j][l] = int(v2, 2)
                        img2[i][j][l] = int(v3, 2)

            cv2.imwrite('./static/uploads/image1.png', img1)
            cv2.imwrite('./static/uploads/image2.png', img2)
            time.sleep(10)
            return render_template("/image_showing.html",umessage="yes")
        except:
            return render_template("/image_showing.html",umessage="SORRY THE IMAGE IS CLEAN AND CLEAR")
    return render_template("/image_showing.html")

@app.route("/decrypt")
def decrypt():
    return render_template("decrypt.html")
@app.route("/decrypt", methods=['GET','POST'])
def decrypt_main():
    if request.method == 'POST':
        try:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                try:
                    text_hidden=lsb.reveal("./static/uploads/" + filename)
                    if text_hidden=="None":
                        text_hidden = "NOTHING IS IN THE IMAGE"



                except:
                    text_hidden="NOTHING IS IN THE IMAGE"
                return render_template("decrypt.html",umessage=text_hidden)
        except:
            return render_template("decrypt.html",umessage="TRY IT AGAIN")
    else:
        return render_template("decrypt.html",umessage="NOT ABLE TO COMPLETE TRY IT AGAIN")


@app.route("/encrypt_decrypt")
def view():
    return render_template("encrypt_decrypt.html")
#
@app.route("/encrypt_decrypt", methods=['GET','POST'])
def encrypt():
    if request.method == 'POST':
        try:

            file = request.files['file']
            text_hidden=request.form["text_hide"]
            print("\n\n\n\n\n\n",text_hidden)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                secret = lsb.hide("./static/uploads/" + filename, text_hidden)
                secret.save("./static/uploads/stegano.png")
                time.sleep(2)
                return render_template("encrypt_decrypt.html",umessage="Yes")
        except:
            return render_template("encrypt_decrypt.html")
    else:
        return render_template("encrypt_decrypt.html")


@app.route("/signup_login_webpage",methods=['GET','POST'])
def index():
    if  request.method=='POST':
        email=request.form['user_email']
        password=request.form['user_pass']
        try:
            auth.sign_in_with_email_and_password(email,password)
            user_info=auth.sign_in_with_email_and_password(email,password)
            account_info=auth.get_account_info(user_info['idToken'])
            orig = email.split("@")

            mesage_first=f"HI {orig[0]}"

            if account_info['users'][0]['emailVerified']==False:
                verify_message="PLEASE VERIFY YOUR EMAIL"
                return render_template("signup_login_webpage.html",umessage=verify_message)
            return render_template('index.html',message=mesage_first)
        except:
            unsuccesful="Please check your credentials"
            return render_template("signup_login_webpage.html",umessage=unsuccesful)
    return render_template("signup_login_webpage.html")


@app.route('/create_account',methods=['GET','POST'])
def create_account():
    if request.method=='POST':
        user_pass0=request.form['user_pass0']
        user_pass1 = request.form['user_pass1']
        if user_pass0==user_pass1:
            try:
                email=request.form['user_email']
                password=request.form['user_pass1']
                new_user=auth.create_user_with_email_and_password(email,password)
                auth.send_email_verification(new_user['idToken'])
                return render_template('verify_email.html')
                # return render_template("index.html")
            except:
                message='THIS EMAIL ALREADY EXIST'
                return render_template('signup_login_webpage.html',exist_message=message)

    return  render_template("create_account.html")

@app.route("/reset_password",methods=['GET','POST'])
def forget_pass():
    if request.method=='POST':
        email=request.form['user_email']
        auth.send_password_reset_email(email)
        return render_template('signup_login_webpage.html')
    return render_template("reset_password.html")

if __name__ == "__main__":
    app.run(debug=True,port=8000)


quit()





