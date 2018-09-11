import os
from flask import Flask, flash, request, redirect, url_for,session
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask import Flask,render_template,url_for,request
import cv2
import numpy as np
from matplotlib import pyplot as plt

UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    
    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>',methods=['GET', 'POST'])
def uploaded_file(filename):
    return render_template('uploaded_file.html',filename = filename)

@app.route('/filter1/<filename>',methods=['GET','POST'])
def filter1(filename):
    img1 = cv2.imread(app.config['UPLOAD_FOLDER']+'/'+filename,1)
    img2 = cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
    output = ''
    x = request.form['effects']
    if x == 'blur':
        output = cv2.blur(img2,(13,13))
    elif x == 'gauss':
        output = cv2.GaussianBlur(img2,(7,7),0)
    elif x == 'denoise':
        output = cv2.medianBlur(img2,3)
    elif x == 'edges':
        output = cv2.Laplacian(img2,-1,ksize=17,scale=1,delta=0,borderType = cv2.BORDER_DEFAULT)
    elif x == 'inpaint':
        output = cv2.inpaint(img2,mask,5,cv2.INPAINT_TELEA)
    elif x == 'inputgrey':
        output = cv2.inpaint(img2,mask,5,cv2.INPAINT_NS)
    else:
        k = np.array(([1,1,0],[1,-4,1],[0,1,0]),np.float32)
        output = cv2.filter2D(img2,-1,k)
    if session.get('filename') == "yes":
        print("entered")
    session['filename']="yes"
    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], "efgh.png"),output)
    return render_template('filter1.html',filename = filename)

@app.route('/filter2/<filename>',methods=['GET','POST'])
def filter2(filename):
    img1 = cv2.imread(app.config['UPLOAD_FOLDER']+'/'+filename,1)
    img2 = cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
    output = ''
    x = request.form['effects']
    if x == 'blur':
        output = cv2.blur(img2,(13,13))
    elif x == 'gauss':
        output = cv2.GaussianBlur(img2,(7,7),0)
    elif x == 'denoise':
        output = cv2.medianBlur(img2,3)
    elif x == 'edges':
        output = cv2.Laplacian(img2,-1,ksize=17,scale=1,delta=0,borderType = cv2.BORDER_DEFAULT)
    elif x == 'inpaint':
        output = cv2.inpaint(img2,mask,5,cv2.INPAINT_TELEA)
    elif x == 'inputgrey':
        output = cv2.inpaint(img2,mask,5,cv2.INPAINT_NS)
    else:
        k = np.array(([1,1,0],[1,-4,1],[0,1,0]),np.float32)
        output = cv2.filter2D(img2,-1,k)
    if session.get('filename') == "yes":
        print("entered")
    session['filename']="yes"
    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], "efgh.png"),output)
    return render_template('filter2.html',filename = filename)
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)