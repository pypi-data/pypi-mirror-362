import cv2
import numpy as np

class MotionDetector:
    def detectMotion(self, frame1, frame2, threshold=30):
        diff = cv2.absdiff(frame1, frame2)
        return np.mean(diff) > threshold

class ColorAnalyzer:
    def dominantColor(self, frame, k=3):
        pixels = frame.reshape(-1, 3)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1)
        _, labels, centers = cv2.kmeans(pixels.astype(np.float32), k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        return centers.astype(int)

class FaceRecognizer:
    def detectFaces(self, frame):
        cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        return cascade.detectMultiScale(frame, 1.1, 4)

class ObjectTracker:
    def trackObject(self, frame, template):
        result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(result)
        return max_loc

class EdgeDetector:
    def detectEdges(self, frame, threshold1=100, threshold2=200):
        return cv2.Canny(frame, threshold1, threshold2)

class FrameComparator:
    def compareFrames(self, frame1, frame2):
        return cv2.matchTemplate(frame1, frame2, cv2.TM_CCOEFF_NORMED)[0][0]

# 独立函数
def readVideoFrames(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        frames.append(frame)
    cap.release()
    return frames

def extractFrameAtTime(video_path, timestamp):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_MSEC, timestamp*1000)
    ret, frame = cap.read()
    cap.release()
    return frame if ret else None

def calculateFrameDifferences(frames):
    return [cv2.absdiff(frames[i], frames[i+1]) for i in range(len(frames)-1)]

def applyGaussianBlur(frame, kernel_size=5):
    return cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)

def detectCorners(frame, max_corners=100, quality=0.01, min_distance=10):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.goodFeaturesToTrack(gray, max_corners, quality, min_distance)

def applyThreshold(frame, threshold=127, max_val=255, type=cv2.THRESH_BINARY):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, threshold, max_val, type)
    return thresh

def findContours(frame, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(gray, mode, method)
    return contours

def drawBoundingBoxes(frame, objects):
    for (x, y, w, h) in objects:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
    return frame

def resizeFrame(frame, width=None, height=None):
    if width and height:
        return cv2.resize(frame, (width, height))
    h, w = frame.shape[:2]
    if width:
        r = width / w
        return cv2.resize(frame, (width, int(h*r)))
    if height:
        r = height / h
        return cv2.resize(frame, (int(w*r), height))
    return frame

def convertColorSpace(frame, code=cv2.COLOR_BGR2GRAY):
    return cv2.cvtColor(frame, code)