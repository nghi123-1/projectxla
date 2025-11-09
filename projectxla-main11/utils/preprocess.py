import cv2
import numpy as np 

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    equalized = cv2.equalizeHist(blur)
    return cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)

def rotate_image(image, angle):
    """Xoay ảnh một góc nhất định."""
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    M[0, 2] += (nW / 2) - center[0]
    M[1, 2] += (nH / 2) - center[1]
    
    rotated = cv2.warpAffine(image, M, (nW, nH))
    return rotated

def convert_to_grayscale(image):
    """Chuyển ảnh sang thang độ xám (3 kênh để hiển thị)."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

def invert_colors(image):
    """Đảo ngược màu ảnh."""
    return cv2.bitwise_not(image)