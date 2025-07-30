import os
import subprocess
from .setup import getFFmpegPath

class VideoConverter:
    def convertFormat(self, input_path, output_path, output_format):
        ffmpeg = getFFmpegPath()
        subprocess.run([ffmpeg, '-i', input_path, output_path + output_format])

class VideoSplitter:
    def splitByTime(self, input_path, start, end, output_path):
        ffmpeg = getFFmpegPath()
        subprocess.run([ffmpeg, '-i', input_path, '-ss', start, '-to', end, '-c', 'copy', output_path])

class VideoMerger:
    def mergeVideos(self, file_list, output_path):
        ffmpeg = getFFmpegPath()
        with open("filelist.txt", "w") as f:
            for file in file_list:
                f.write(f"file '{file}'\n")
        subprocess.run([ffmpeg, '-f', 'concat', '-safe', '0', '-i', 'filelist.txt', '-c', 'copy', output_path])

class ResolutionScaler:
    def scaleResolution(self, input_path, width, height, output_path):
        ffmpeg = getFFmpegPath()
        subprocess.run([ffmpeg, '-i', input_path, '-vf', f'scale={width}:{height}', output_path])

class FrameRateModifier:
    def changeFrameRate(self, input_path, fps, output_path):
        ffmpeg = getFFmpegPath()
        subprocess.run([ffmpeg, '-i', input_path, '-r', str(fps), output_path])

class VideoValidator:
    def checkIntegrity(self, input_path):
        ffmpeg = getFFmpegPath()
        result = subprocess.run([ffmpeg, '-v', 'error', '-i', input_path, '-f', 'null', '-'], capture_output=True)
        return result.stderr.decode()

# 独立函数
def extractThumbnail(input_path, time, output_path):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-ss', time, '-vframes', '1', output_path])

def getVideoDuration(input_path):
    ffmpeg = getFFmpegPath()
    result = subprocess.run([ffmpeg, '-i', input_path], capture_output=True, text=True)
    return result.stderr

def generatePreview(input_path, output_path, duration=10):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-t', str(duration), output_path])

def addWatermark(input_path, image_path, output_path, position="10:10"):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-i', image_path, 
                   '-filter_complex', f'overlay={position}', output_path])

def removeAudio(input_path, output_path):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-an', output_path])

def rotateVideo(input_path, degrees, output_path):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-vf', f"rotate={degrees}*PI/180", output_path])

def cropVideo(input_path, x, y, width, height, output_path):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-filter:v', f"crop={width}:{height}:{x}:{y}", output_path])

def changeAspectRatio(input_path, ratio, output_path):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-aspect', str(ratio), output_path])

def addSubtitles(input_path, srt_path, output_path):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-vf', f"subtitles={srt_path}", output_path])

def extractFrames(input_path, output_pattern):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, output_pattern])