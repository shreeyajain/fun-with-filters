import cv2

def dodgeV2(image, mask):
    return cv2.divide(image, 255 - mask, scale = 256)

# function to convert each frame into a pencil sketch
def pencil_sketch(frame):
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        invert = cv2.bitwise_not(gray)
        smooth = cv2.GaussianBlur(invert, (21, 21), sigmaX = 0, sigmaY = 0)
        frame = dodgeV2(gray, smooth)
        
    except Exception as e:
        pass

    return frame