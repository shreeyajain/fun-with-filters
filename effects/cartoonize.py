import cv2

def edge_mask(img, line_size, blur_value):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, blur_value)
    edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, line_size, blur_value)
    return edges

# function to convert each frame into a cartoon version
def cartoonize(frame):
    try:
        edges = edge_mask(frame, 7, 5)
        blurred = cv2.bilateralFilter(frame, 7, 150, 150)
        frame = cv2.bitwise_and(blurred, blurred, mask = edges)

    except Exception as e:
        pass

    return frame