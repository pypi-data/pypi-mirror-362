import subprocess
from .setup import getFFmpegPath

class CodecInfoExtractor:
    def getCodecInfo(self, video_path):
        ffmpeg = getFFmpegPath()
        result = subprocess.run([ffmpeg, '-i', video_path], capture_output=True, text=True)
        return result.stderr

class CodecChanger:
    def changeVideoCodec(self, input_path, output_path, codec='libx264'):
        ffmpeg = getFFmpegPath()
        subprocess.run([ffmpeg, '-i', input_path, '-c:v', codec, output_path])

class BitrateController:
    def adjustBitrate(self, input_path, output_path, bitrate='2000k'):
        ffmpeg = getFFmpegPath()
        subprocess.run([ffmpeg, '-i', input_path, '-b:v', bitrate, output_path])

class CRFAdjuster:
    def setCRF(self, input_path, output_path, crf=23):
        ffmpeg = getFFmpegPath()
        subprocess.run([ffmpeg, '-i', input_path, '-crf', str(crf), output_path])

class ProfileSetter:
    def setProfile(self, input_path, output_path, profile='high'):
        ffmpeg = getFFmpegPath()
        subprocess.run([ffmpeg, '-i', input_path, '-profile:v', profile, output_path])

class PresetApplier:
    def applyPreset(self, input_path, output_path, preset='slow'):
        ffmpeg = getFFmpegPath()
        subprocess.run([ffmpeg, '-i', input_path, '-preset', preset, output_path])

# 独立函数
def checkCodecSupport(codec_name):
    ffmpeg = getFFmpegPath()
    result = subprocess.run([ffmpeg, '-codecs'], capture_output=True, text=True)
    return codec_name in result.stdout

def getSupportedFormats():
    ffmpeg = getFFmpegPath()
    result = subprocess.run([ffmpeg, '-formats'], capture_output=True, text=True)
    return result.stdout

def convertToH265(input_path, output_path):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-c:v', 'libx265', output_path])

def convertToVP9(input_path, output_path):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-c:v', 'libvpx-vp9', output_path])

def extractKeyframes(input_path, output_pattern):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-vf', "select='eq(pict_type,PICT_TYPE_I)'", '-vsync', 'vfr', output_pattern])

def applyLosslessCompression(input_path, output_path):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-crf', '0', output_path])

def setKeyframeInterval(input_path, output_path, interval=30):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-g', str(interval), output_path])

def addBFrame(input_path, output_path, bframes=3):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-bf', str(bframes), output_path])

def changeColorSpace(input_path, output_path, colorspace='bt709'):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-colorspace', colorspace, output_path])

def setAudioCodec(input_path, output_path, codec='aac'):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-c:a', codec, output_path])