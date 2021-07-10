import cv2
import numpy as np

# function to crop each camera frame and display just the face using a
# pretrained face detection model
def detect_face(frame):
    # load the pretrained face detection model    
    net = cv2.dnn.readNetFromCaffe('./effects/pretrained_model/deploy.prototxt.txt', 
        './effects/pretrained_model/res10_300x300_ssd_iter_140000.caffemodel')

    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0))   
    net.setInput(blob)
    detections = net.forward()
    confidence = detections[0, 0, 0, 2]

    if confidence < 0.5:            
        return frame           

    box = detections[0, 0, 0, 3:7] * np.array([w, h, w, h])
    (startX, startY, endX, endY) = box.astype("int")

    try:
        frame = frame[startY:endY, startX:endX]
        (h, w) = frame.shape[:2]
        r = 480 / float(h)
        dim = ( int(w * r), 480)
        frame = cv2.resize(frame, dim)

    except Exception as e:
        pass

    return frame