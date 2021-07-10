# import the necessary libraries
from flask import Flask, render_template, Response, request
import cv2
import datetime, time
import os

# import the effect modules
from effects.pencil_sketch import *
from effects.cartoonize import *
from effects.detect_face import *

# declare the global variables
global switch, gray, negative, pencil, cartoon, face, capture, effect_sel
switch = 1
gray = negative = pencil = cartoon = face = capture = 0
effect_sel = 'original'

# create gallery directory to save pictures
try:
    os.mkdir('./gallery')
except OSError as error:
    pass

# instatiate the flask app  
app = Flask(__name__, template_folder='./templates')

camera = cv2.VideoCapture(0)

# function to capture and process the webcam frames
def gen_frames():
    global capture, effect_sel
    while True:
        success, frame = camera.read() 
        if success:
            if gray:
                effect_sel = 'gray'
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
            if negative:
                effect_sel = 'negative'
                frame = cv2.bitwise_not(frame)
                
            if pencil:
                effect_sel = 'pencil_sketch'
                frame = pencil_sketch(frame)
                
            if cartoon:
                effect_sel = 'cartoon'
                frame = cartoonize(frame)
                
            if face:
                effect_sel = 'face_only'
                frame = detect_face(frame)
             
            if capture:
                capture = 0
                now = datetime.datetime.now()
                p = os.path.sep.join(['gallery', str(effect_sel) + 
                    '_{}.png'.format(str(now).replace(":",''))])
                cv2.imwrite(p, frame)
            
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests', methods=['POST','GET'])
def tasks():
    global switch, camera, gray, negative, pencil, cartoon, face, effect_sel
    if request.method == 'POST':
        
        if request.form.get('stop') == 'Stop/Start':
            if switch == 1:
                switch = 0
                camera.release()
                cv2.destroyAllWindows()    
            else:
                camera = cv2.VideoCapture(0)
                switch = 1
                gray = negative = pencil = cartoon = face = 0
                effect_sel = 'original'
                
        elif request.form.get('gray') == 'Gray':
            gray = not gray
            negative = pencil = cartoon = face = 0
            if not gray:
                effect_sel = 'original'
            
        elif request.form.get('negative') == 'Negative':
            negative = not negative
            gray = pencil = cartoon = face = 0
            if not negative:
                effect_sel = 'original'
            
        elif request.form.get('pencil') == 'Pencil Sketch':
            pencil = not pencil
            gray = negative = cartoon = face = 0
            if not pencil:
                effect_sel = 'original'
            
        elif request.form.get('cartoon') == 'Cartoon':
            cartoon = not cartoon
            gray = negative = pencil = face = 0
            if not cartoon:
                effect_sel = 'original'
        
        elif request.form.get('face') == 'Face Only':
            face = not face 
            gray = negative = pencil = cartoon = 0
            if face:
                time.sleep(4)
            if not face:
                effect_sel = 'original'
                
        elif request.form.get('click') == 'Capture':
            global capture
            capture = 1
                                      
    elif request.method=='GET':
        return render_template('index.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.run()