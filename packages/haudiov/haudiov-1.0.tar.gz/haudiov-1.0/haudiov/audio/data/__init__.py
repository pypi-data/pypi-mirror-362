# 标识data为Python包
class DataPackageInfo:
    """数据包信息类"""
    def __init__(self):
        self.version = "1.0"
        self.author = "AudioProcessor Team"
    
    def getInfo(self):
        """获取包信息"""
        return f"Audio Processor Data Package v{self.version} by {self.author}"

class AudioFormat:
    """音频格式常量"""
    MP3 = "mp3"
    WAV = "wav"
    FLAC = "flac"
    AAC = "aac"
    OGG = "ogg"

class CodecLibrary:
    """编解码器库常量"""
    MP3 = "libmp3lame"
    AAC = "aac"
    FLAC = "flac"
    OPUS = "libopus"
    VORBIS = "libvorbis"

class BitratePreset:
    """比特率预设"""
    LOW = "64k"
    MEDIUM = "128k"
    HIGH = "192k"
    VERY_HIGH = "320k"

class SampleRatePreset:
    """采样率预设"""
    CD = 44100
    DVD = 48000
    HIGH = 96000

class ChannelLayout:
    """声道布局"""
    MONO = 1
    STEREO = 2
    SURROUND_5_1 = 6

# 包初始化时创建实例
packageInfo = DataPackageInfo()
audioFormat = AudioFormat()
codecLibrary = CodecLibrary()
bitratePreset = BitratePreset()
sampleRatePreset = SampleRatePreset()
channelLayout = ChannelLayout()