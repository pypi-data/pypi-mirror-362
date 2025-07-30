from .. import AudioProcessorBase, AudioConvertInterface
import os

class ConvertConfig:
    """转换配置类"""
    def __init__(self):
        self.codec = "libmp3lame"
        self.bitrate = "192k"
        self.sampleRate = 44100
        self.channels = 2
        self.quality = 2
        self.normalize = False

class ConvertResult:
    """转换结果类"""
    def __init__(self, success, inputFormat, outputFormat, outputPath, message=""):
        self.success = success
        self.inputFormat = inputFormat
        self.outputFormat = outputFormat
        self.outputPath = outputPath
        self.message = message
    
    def __str__(self):
        return f"Converted {self.inputFormat} to {self.outputFormat}: {'Success' if self.success else 'Failed'}"

class ConvertProgress:
    """转换进度类"""
    def __init__(self):
        self.percentage = 0
        self.currentTime = 0
        self.totalTime = 0
    
    def update(self, percentage, currentTime, totalTime):
        """更新进度"""
        self.percentage = percentage
        self.currentTime = currentTime
        self.totalTime = totalTime

class ConvertError(Exception):
    """转换错误异常类"""
    def __init__(self, message, errorCode):
        super().__init__(message)
        self.errorCode = errorCode

class AudioConverter(AudioProcessorBase, AudioConvertInterface):
    """音频转换器"""
    def __init__(self):
        super().__init__()
        self.config = ConvertConfig()
    
    def convertFormat(self, inputPath, outputPath, codec="libmp3lame", bitrate="192k"):
        """转换音频格式"""
        self.validateInputFile(inputPath)
        self.validateOutputPath(outputPath)
        
        inputExt = self.getFileExtension(inputPath)
        outputExt = self.getFileExtension(outputPath)
        
        command = [
            "-y",
            "-i", inputPath,
            "-c:a", codec,
            "-b:a", bitrate,
            outputPath
        ]
        
        try:
            self.runFfmpegCommand(command)
            return ConvertResult(True, inputExt, outputExt, outputPath, "Conversion successful")
        except Exception as e:
            return ConvertResult(False, inputExt, outputExt, outputPath, str(e))
    
    def changeSampleRate(self, inputPath, outputPath, sampleRate=44100):
        """更改采样率"""
        self.validateInputFile(inputPath)
        self.validateOutputPath(outputPath)
        
        command = [
            "-y",
            "-i", inputPath,
            "-ar", str(sampleRate),
            outputPath
        ]
        
        try:
            self.runFfmpegCommand(command)
            return True
        except Exception as e:
            raise ConvertError(f"Sample rate change failed: {str(e)}", 3001)
    
    def changeChannels(self, inputPath, outputPath, channels=2):
        """更改声道数"""
        self.validateInputFile(inputPath)
        self.validateOutputPath(outputPath)
        
        command = [
            "-y",
            "-i", inputPath,
            "-ac", str(channels),
            outputPath
        ]
        
        try:
            self.runFfmpegCommand(command)
            return True
        except Exception as e:
            raise ConvertError(f"Channel change failed: {str(e)}", 3002)
    
    def extractMetadata(self, inputPath, outputPath):
        """提取元数据到单独文件"""
        self.validateInputFile(inputPath)
        self.validateOutputPath(outputPath)
        
        command = [
            "-y",
            "-i", inputPath,
            "-f", "ffmetadata",
            outputPath
        ]
        
        try:
            self.runFfmpegCommand(command)
            return True
        except Exception as e:
            raise ConvertError(f"Metadata extraction failed: {str(e)}", 3003)
    
    def addMetadata(self, inputPath, outputPath, metadataFile):
        """从文件添加元数据"""
        self.validateInputFile(inputPath)
        self.validateOutputPath(outputPath)
        self.validateInputFile(metadataFile)
        
        command = [
            "-y",
            "-i", inputPath,
            "-i", metadataFile,
            "-map_metadata", "1",
            "-c", "copy",
            outputPath
        ]
        
        try:
            self.runFfmpegCommand(command)
            return True
        except Exception as e:
            raise ConvertError(f"Metadata addition failed: {str(e)}", 3004)
    
    def setBitrateMode(self, inputPath, outputPath, mode="vbr", quality=2):
        """设置比特率模式"""
        self.validateInputFile(inputPath)
        self.validateOutputPath(outputPath)
        
        codec = self.getCodecFromExtension(outputPath)
        if not codec:
            raise ConvertError("Unsupported output format", 3005)
        
        command = ["-y", "-i", inputPath]
        
        if mode == "vbr":
            command += ["-q:a", str(quality)]
        elif mode == "cbr":
            command += ["-b:a", self.config.bitrate]
        else:
            raise ConvertError("Invalid bitrate mode", 3006)
        
        command.append(outputPath)
        
        try:
            self.runFfmpegCommand(command)
            return True
        except Exception as e:
            raise ConvertError(f"Bitrate mode change failed: {str(e)}", 3007)
    
    def normalizeAudio(self, inputPath, outputPath):
        """标准化音频音量"""
        command = [
            "-y",
            "-i", inputPath,
            "-af", "loudnorm",
            outputPath
        ]
        
        try:
            self.runFfmpegCommand(command)
            return True
        except Exception as e:
            raise ConvertError(f"Normalization failed: {str(e)}", 3008)
    
    def getFileExtension(self, filePath):
        """获取文件扩展名"""
        return os.path.splitext(filePath)[1][1:].lower()
    
    def getCodecFromExtension(self, filePath):
        """根据扩展名获取编解码器"""
        ext = self.getFileExtension(filePath)
        codecMap = {
            "mp3": "libmp3lame",
            "wav": "pcm_s16le",
            "flac": "flac",
            "aac": "aac",
            "ogg": "libvorbis"
        }
        return codecMap.get(ext, None)
    
    def setCodec(self, codec):
        """设置编解码器"""
        self.config.codec = codec
    
    def setBitrate(self, bitrate):
        """设置比特率"""
        self.config.bitrate = bitrate
    
    def setSampleRate(self, sampleRate):
        """设置采样率"""
        self.config.sampleRate = sampleRate
    
    def setChannels(self, channels):
        """设置声道数"""
        self.config.channels = channels

class ConvertUtils:
    """转换工具类"""
    @staticmethod
    def getSupportedFormats():
        """获取支持的格式"""
        return ["mp3", "wav", "flac", "aac", "ogg", "m4a", "wma"]
    
    @staticmethod
    def formatToExtension(formatName):
        """格式名转扩展名"""
        formatMap = {
            "mp3": "mp3",
            "wav": "wav",
            "flac": "flac",
            "aac": "aac",
            "ogg": "ogg",
            "m4a": "m4a",
            "wma": "wma"
        }
        return formatMap.get(formatName.lower(), "mp3")
    
    @staticmethod
    def isValidBitrate(bitrate):
        """验证比特率是否有效"""
        if not bitrate.endswith('k'):
            return False
        try:
            value = int(bitrate[:-1])
            return 8 <= value <= 320
        except ValueError:
            return False
    
    @staticmethod
    def isValidSampleRate(sampleRate):
        """验证采样率是否有效"""
        return sampleRate in [8000, 11025, 16000, 22050, 44100, 48000, 96000]

class ConvertFactory:
    """转换工厂类"""
    @staticmethod
    def createConverter(config=None):
        """创建转换器实例"""
        converter = AudioConverter()
        if config:
            converter.config = config
        return converter
    
    @staticmethod
    def createDefaultConfig():
        """创建默认配置"""
        return ConvertConfig()

class ConvertValidator:
    """转换验证器"""
    @staticmethod
    def validateCodec(codec):
        """验证编解码器"""
        supportedCodecs = ["libmp3lame", "aac", "flac", "libvorbis", "pcm_s16le"]
        if codec not in supportedCodecs:
            raise ValueError(f"Unsupported codec: {codec}")
        return True
    
    @staticmethod
    def validateOutputFormat(inputFormat, outputFormat):
        """验证输出格式"""
        # 实际应检查是否支持转换
        return inputFormat != outputFormat