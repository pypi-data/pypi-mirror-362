from .. import AudioProcessorBase, AudioExtractInterface
import os

class ExtractConfig:
    """提取配置类"""
    def __init__(self):
        self.codec = "pcm_s16le"
        self.bitrate = "192k"
        self.sampleRate = 44100
        self.channels = 2
        self.extractAllTracks = False
        self.keepVideo = False

class ExtractResult:
    """提取结果类"""
    def __init__(self, success, outputPaths, trackCount, message=""):
        self.success = success
        self.outputPaths = outputPaths
        self.trackCount = trackCount
        self.message = message
    
    def __str__(self):
        return f"Extracted {self.trackCount} tracks: {'Success' if self.success else 'Failed'}"

class ExtractProgress:
    """提取进度类"""
    def __init__(self):
        self.percentage = 0
        self.currentTime = 0
        self.totalTime = 0
    
    def update(self, percentage, currentTime, totalTime):
        """更新进度"""
        self.percentage = percentage
        self.currentTime = currentTime
        self.totalTime = totalTime

class ExtractError(Exception):
    """提取错误异常类"""
    def __init__(self, message, errorCode):
        super().__init__(message)
        self.errorCode = errorCode

class AudioExtractor(AudioProcessorBase, AudioExtractInterface):
    """音频提取器"""
    def __init__(self):
        super().__init__()
        self.config = ExtractConfig()
    
    def extractFromVideo(self, videoPath, outputPath):
        """从视频提取音频"""
        self.validateInputFile(videoPath)
        self.validateOutputPath(outputPath)
        
        command = [
            "-y",
            "-i", videoPath,
            "-vn",  # 禁用视频
            "-acodec", self.config.codec,
            outputPath
        ]
        
        try:
            self.runFfmpegCommand(command)
            return ExtractResult(True, [outputPath], 1, "Audio extracted successfully")
        except Exception as e:
            return ExtractResult(False, [outputPath], 0, str(e))
    
    def extractMultipleTracks(self, videoPath, outputPattern, trackIndices=[0]):
        """提取多个音轨"""
        self.validateInputFile(videoPath)
        
        outputPaths = []
        commands = []
        
        for index in trackIndices:
            outputPath = outputPattern.replace("%d", str(index))
            self.validateOutputPath(outputPath)
            outputPaths.append(outputPath)
            
            command = [
                "-y",
                "-i", videoPath,
                "-map", f"0:a:{index}",
                "-acodec", self.config.codec,
                outputPath
            ]
            commands.append(command)
        
        results = []
        for cmd in commands:
            try:
                self.runFfmpegCommand(cmd)
                results.append(True)
            except Exception as e:
                results.append(False)
        
        success = all(results)
        return ExtractResult(success, outputPaths, len(trackIndices),
                            "All tracks extracted" if success else "Some tracks failed to extract")
    
    def extractWithVideo(self, videoPath, outputPath):
        """提取音频但保留视频流（静音）"""
        self.validateInputFile(videoPath)
        self.validateOutputPath(outputPath)
        
        command = [
            "-y",
            "-i", videoPath,
            "-c:v", "copy",
            "-an",  # 禁用音频
            outputPath
        ]
        
        try:
            self.runFfmpegCommand(command)
            return True
        except Exception as e:
            raise ExtractError(f"Extract with video failed: {str(e)}", 4001)
    
    def convertWhileExtracting(self, videoPath, outputPath, codec="libmp3lame"):
        """提取时转换格式"""
        self.validateInputFile(videoPath)
        self.validateOutputPath(outputPath)
        
        command = [
            "-y",
            "-i", videoPath,
            "-vn",
            "-acodec", codec,
            outputPath
        ]
        
        try:
            self.runFfmpegCommand(command)
            return True
        except Exception as e:
            raise ExtractError(f"Convert while extracting failed: {str(e)}", 4002)
    
    def extractToWav(self, videoPath, outputPath):
        """提取为WAV格式"""
        return self.convertWhileExtracting(videoPath, outputPath, "pcm_s16le")
    
    def extractToMp3(self, videoPath, outputPath):
        """提取为MP3格式"""
        return self.convertWhileExtracting(videoPath, outputPath, "libmp3lame")
    
    def extractClip(self, videoPath, outputPath, startTime, duration):
        """提取音频片段"""
        self.validateInputFile(videoPath)
        self.validateOutputPath(outputPath)
        
        startFormatted = self.formatTime(startTime)
        durationFormatted = self.formatTime(duration)
        
        command = [
            "-y",
            "-ss", startFormatted,
            "-i", videoPath,
            "-t", durationFormatted,
            "-vn",
            "-acodec", self.config.codec,
            outputPath
        ]
        
        try:
            self.runFfmpegCommand(command)
            return True
        except Exception as e:
            raise ExtractError(f"Clip extraction failed: {str(e)}", 4003)
    
    def getAudioTrackCount(self, videoPath):
        """获取音轨数量"""
        self.validateInputFile(videoPath)
        
        command = [
            "-i", videoPath
        ]
        
        try:
            result = self.runFfmpegCommand(command)
        except RuntimeError as e:
            # 元数据通常在错误输出中
            result = str(e)
        
        # 解析输出获取音轨数量
        return self.parseTrackCount(result)
    
    def parseTrackCount(self, output):
        """解析FFmpeg输出获取音轨数量"""
        import re
        count = 0
        
        # 正则表达式匹配音轨信息
        audio_stream_pattern = re.compile(
            r'Stream\s+#\d+:\d+\(?.*?\)?:\s+Audio:'
        )
        
        # 检查输出中所有匹配的音轨
        for line in output.split('\n'):
            if audio_stream_pattern.search(line):
                count += 1
        
        return count
    
    def setCodec(self, codec):
        """设置编解码器"""
        self.config.codec = codec
    
    def setExtractAllTracks(self, extractAll):
        """设置是否提取所有音轨"""
        self.config.extractAllTracks = extractAll
    
    def setKeepVideo(self, keepVideo):
        """设置是否保留视频"""
        self.config.keepVideo = keepVideo

class ExtractUtils:
    """提取工具类"""
    @staticmethod
    def generateOutputPath(videoPath, trackIndex=0, extension="wav"):
        """生成输出路径"""
        baseName = os.path.splitext(os.path.basename(videoPath))[0]
        return f"{baseName}_track{trackIndex}.{extension}"
    
    @staticmethod
    def getDefaultCodecForFormat(format):
        """获取格式的默认编解码器"""
        codecMap = {
            "wav": "pcm_s16le",
            "mp3": "libmp3lame",
            "flac": "flac",
            "aac": "aac",
            "ogg": "libvorbis"
        }
        return codecMap.get(format.lower(), "pcm_s16le")
    
    @staticmethod
    def isValidTrackIndex(index, maxTracks):
        """验证音轨索引是否有效"""
        return 0 <= index < maxTracks
    
    @staticmethod
    def formatTrackIndices(indices, maxTracks):
        """格式化音轨索引列表"""
        validIndices = [idx for idx in indices if 0 <= idx < maxTracks]
        return validIndices if validIndices else [0]

class ExtractFactory:
    """提取工厂类"""
    @staticmethod
    def createExtractor(config=None):
        """创建提取器实例"""
        extractor = AudioExtractor()
        if config:
            extractor.config = config
        return extractor
    
    @staticmethod
    def createDefaultConfig():
        """创建默认配置"""
        return ExtractConfig()

class ExtractValidator:
    """提取验证器"""
    @staticmethod
    def validateVideoFile(videoPath):
        """验证视频文件"""
        if not videoPath.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.flv')):
            raise ValueError("Unsupported video format")
        return True
    
    @staticmethod
    def validateTrackIndices(indices, maxTracks):
        """验证音轨索引"""
        if not indices:
            raise ValueError("No track indices provided")
        
        for idx in indices:
            if not (0 <= idx < maxTracks):
                raise ValueError(f"Invalid track index: {idx}")
        return True