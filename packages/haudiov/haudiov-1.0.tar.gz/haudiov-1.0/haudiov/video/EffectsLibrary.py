import cv2
import numpy as np

class FilterApplier:
    def applySepia(self, frame):
        sepia_filter = np.array([[0.272, 0.534, 0.131],
                                [0.349, 0.686, 0.168],
                                [0.393, 0.769, 0.189]])
        return cv2.transform(frame, sepia_filter)

class TransitionMaker:
    def fadeTransition(self, frame1, frame2, alpha):
        return cv2.addWeighted(frame1, alpha, frame2, 1-alpha, 0)

class TextOverlayer:
    def addText(self, frame, text, position, font_scale=1, color=(0,0,255), thickness=2):
        return cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)

class ZoomEffect:
    def applyZoom(self, frame, factor):
        h, w = frame.shape[:2]
        center = (w//2, h//2)
        M = cv2.getRotationMatrix2D(center, 0, factor)
        return cv2.warpAffine(frame, M, (w, h))

class Stabilizer:
    def stabilizeFrame(self, prev_frame, curr_frame):
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        transform = cv2.estimateAffinePartial2D(prev_gray, curr_gray)[0]
        return cv2.warpAffine(curr_frame, transform, (curr_frame.shape[1], curr_frame.shape[0]))

class SlowMotionGenerator:
    def generateSlowMotion(self, frames, factor=2):
        return [frame for frame in frames for _ in range(factor)]

# 独立函数
def applyGrayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def applyInvert(frame):
    return cv2.bitwise_not(frame)

def applySketchEffect(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    inverted = 255 - gray
    blurred = cv2.GaussianBlur(inverted, (21,21), 0)
    return cv2.divide(gray, 255-blurred, scale=256)

def applyVignette(frame, level=2):
    h, w = frame.shape[:2]
    kernel_x = cv2.getGaussianKernel(w, w/level)
    kernel_y = cv2.getGaussianKernel(h, h/level)
    kernel = kernel_y * kernel_x.T
    mask = kernel / kernel.max()
    return frame * np.expand_dims(mask, axis=2)

def applyPixelation(frame, pixel_size=8):
    h, w = frame.shape[:2]
    temp = cv2.resize(frame, (w//pixel_size, h//pixel_size), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)

def applyBlur(frame, intensity=5):
    return cv2.blur(frame, (intensity, intensity))

def applySharpen(frame):
    kernel = np.array([[-1,-1,-1], 
                      [-1,9,-1], 
                      [-1,-1,-1]])
    return cv2.filter2D(frame, -1, kernel)

def applyEdgeGlow(frame):
    edges = cv2.Canny(frame, 100, 200)
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    return cv2.addWeighted(frame, 0.8, edges, 0.2, 0)

def applyColorOverlay(frame, color=(25,25,180)):
    overlay = np.full_like(frame, color)
    return cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)

def applyOldFilmEffect(frame):
    # 添加噪点
    noise = np.random.randint(0,50,frame.shape[:2], dtype=np.uint8)
    noise = np.repeat(noise[:, :, np.newaxis], 3, axis=2)
    frame = cv2.add(frame, noise)
    
    # 添加划痕
    scratches = np.zeros_like(frame)
    for _ in range(5):
        x = np.random.randint(0, frame.shape[1])
        cv2.line(scratches, (x,0), (x,frame.shape[0]), (200,200,200), 1)
    frame = cv2.addWeighted(frame, 0.9, scratches, 0.1, 0)
    
    return frame