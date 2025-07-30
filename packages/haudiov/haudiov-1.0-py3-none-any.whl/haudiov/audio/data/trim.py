from .. import AudioProcessorBase, AudioTrimInterface
import os

class TrimConfig:
    """裁剪配置类"""
    def __init__(self):
        self.preciseCut = True
        self.copyCodec = False
        self.silenceThreshold = -30
        self.fadeInDuration = 0.5
        self.fadeOutDuration = 0.5

class TrimResult:
    """裁剪结果类"""
    def __init__(self, success, outputPath, duration, message=""):
        self.success = success
        self.outputPath = outputPath
        self.duration = duration
        self.message = message
    
    def __str__(self):
        return f"Trim {'successful' if self.success else 'failed'}: {self.message}"

class TrimProgress:
    """裁剪进度类"""
    def __init__(self):
        self.percentage = 0
        self.currentTime = 0
        self.totalTime = 0
    
    def update(self, percentage, currentTime, totalTime):
        """更新进度"""
        self.percentage = percentage
        self.currentTime = currentTime
        self.totalTime = totalTime

class TrimError(Exception):
    """裁剪错误异常类"""
    def __init__(self, message, errorCode):
        super().__init__(message)
        self.errorCode = errorCode

class AudioTrimmer(AudioProcessorBase, AudioTrimInterface):
    """音频裁剪器"""
    def __init__(self):
        super().__init__()
        self.config = TrimConfig()
    
    def trimAudio(self, inputPath, outputPath, startTime, duration):
        """裁剪音频文件"""
        self.validateInputFile(inputPath)
        self.validateOutputPath(outputPath)
        
        startFormatted = self.formatTime(startTime)
        durationFormatted = self.formatTime(duration)
        
        command = [
            "-y",
            "-ss", startFormatted,
            "-i", inputPath,
            "-t", durationFormatted,
            "-c:a", "copy" if self.config.copyCodec else "libmp3lame",
            outputPath
        ]
        
        try:
            self.runFfmpegCommand(command)
            return TrimResult(True, outputPath, duration, "Trim completed successfully")
        except Exception as e:
            return TrimResult(False, outputPath, 0, str(e))
    
    def trimToEnd(self, inputPath, outputPath, startTime):
        """从开始时间裁剪到文件末尾"""
        self.validateInputFile(inputPath)
        self.validateOutputPath(outputPath)
        
        startFormatted = self.formatTime(startTime)
        
        command = [
            "-y",
            "-ss", startFormatted,
            "-i", inputPath,
            "-c:a", "copy" if self.config.copyCodec else "libmp3lame",
            outputPath
        ]
        
        try:
            self.runFfmpegCommand(command)
            return TrimResult(True, outputPath, 0, "Trim to end completed")
        except Exception as e:
            return TrimResult(False, outputPath, 0, str(e))
    
    def trimSilence(self, inputPath, outputPath, threshold=-30):
        """裁剪静音部分"""
        self.validateInputFile(inputPath)
        self.validateOutputPath(outputPath)
        
        command = [
            "-y",
            "-i", inputPath,
            "-af", f"silenceremove=start_periods=1:start_threshold={threshold}dB",
            outputPath
        ]
        
        try:
            self.runFfmpegCommand(command)
            return TrimResult(True, outputPath, 0, "Silence removal completed")
        except Exception as e:
            return TrimResult(False, outputPath, 0, str(e))
    
    def fadeIn(self, inputPath, outputPath, duration=1.0):
        """添加淡入效果"""
        return self.applyFade(inputPath, outputPath, "in", duration)
    
    def fadeOut(self, inputPath, outputPath, duration=1.0):
        """添加淡出效果"""
        return self.applyFade(inputPath, outputPath, "out", duration)
    
    def applyFade(self, inputPath, outputPath, fadeType, duration):
        """应用淡入淡出效果"""
        self.validateInputFile(inputPath)
        self.validateOutputPath(outputPath)
        
        if fadeType not in ["in", "out"]:
            raise ValueError("Invalid fade type. Use 'in' or 'out'")
        
        command = [
            "-y",
            "-i", inputPath,
            "-af", f"afade=t={fadeType}:d={duration}",
            outputPath
        ]
        
        try:
            self.runFfmpegCommand(command)
            return True
        except Exception as e:
            raise TrimError(f"Fade {fadeType} failed: {str(e)}", 1001)
    
    def splitByDuration(self, inputPath, outputPattern, segmentDuration):
        """按持续时间分割音频"""
        self.validateInputFile(inputPath)
        
        command = [
            "-y",
            "-i", inputPath,
            "-f", "segment",
            "-segment_time", str(segmentDuration),
            "-c", "copy",
            outputPattern
        ]
        
        try:
            self.runFfmpegCommand(command)
            return True
        except Exception as e:
            raise TrimError(f"Split failed: {str(e)}", 1002)
    
    def splitBySilence(self, inputPath, outputPattern, silenceThreshold=-30, minSilenceDuration=0.5):
        """按静音分割音频"""
        self.validateInputFile(inputPath)
        
        command = [
            "-y",
            "-i", inputPath,
            "-f", "segment",
            "-segment_times", self.detectSilence(inputPath, silenceThreshold, minSilenceDuration),
            "-c", "copy",
            outputPattern
        ]
        
        try:
            self.runFfmpegCommand(command)
            return True
        except Exception as e:
            raise TrimError(f"Silence split failed: {str(e)}", 1003)
    
    def detectSilence(self, inputPath, threshold=-30, minDuration=0.5):
        """检测静音位置"""
        self.validateInputFile(inputPath)
        
        command = [
            "-i", inputPath,
            "-af", f"silencedetect=n={threshold}dB:d={minDuration}",
            "-f", "null",
            "-"
        ]
        
        try:
            result = self.runFfmpegCommand(command)
            # 解析结果获取静音位置
            return self.parseSilenceDetect(result)
        except Exception as e:
            raise TrimError(f"Silence detection failed: {str(e)}", 1004)
    
    def parseSilenceDetect(self, output):
        """解析FFmpeg静音检测输出，返回静音结束时间点列表"""
        import re
        pattern = r"silence_end:\s*(\d+\.\d+)"
        matches = re.findall(pattern, output)
        silence_ends = sorted(float(match) for match in matches)
        return ",".join(map(str, silence_ends))
    
    def setPreciseCut(self, precise):
        """设置精确裁剪模式"""
        self.config.preciseCut = precise
    
    def setCopyCodec(self, copy):
        """设置是否复制编解码器"""
        self.config.copyCodec = copy
    
    def setFadeDurations(self, fadeIn, fadeOut):
        """设置淡入淡出持续时间"""
        self.config.fadeInDuration = fadeIn
        self.config.fadeOutDuration = fadeOut

class TrimUtils:
    """裁剪工具类"""
    @staticmethod
    def calculateSegmentCount(totalDuration, segmentDuration):
        """计算分段数量"""
        return int(totalDuration // segmentDuration) + (1 if totalDuration % segmentDuration > 0 else 0)
    
    @staticmethod
    def validateDuration(duration):
        """验证持续时间是否有效"""
        if duration <= 0:
            raise ValueError("Duration must be positive")
        return True
    
    @staticmethod
    def formatOutputPattern(pattern, index):
        """格式化输出模式"""
        return pattern.replace("%d", str(index))
    
    @staticmethod
    def getFileDuration(inputPath):
        import re
        """获取音频文件总时长（秒）"""
        from .. import AudioProcessorBase
        processor = AudioProcessorBase()
        
        try:
            metadata = processor.getFileMetadata(inputPath)
            duration_match = re.search(
                r'Duration:\s(\d+):(\d+):(\d+\.\d+)', 
                metadata
            )
            
            if duration_match:
                hours = int(duration_match.group(1))
                minutes = int(duration_match.group(2))
                seconds = float(duration_match.group(3))
                return hours * 3600 + minutes * 60 + seconds
        except Exception:
            pass
        
        return 0.0
    
    @staticmethod
    def normalizeThreshold(threshold):
        """标准化阈值"""
        return max(-60, min(0, threshold))

class TrimFactory:
    """裁剪工厂类"""
    @staticmethod
    def createTrimmer(config=None):
        """创建裁剪器实例"""
        trimmer = AudioTrimmer()
        if config:
            trimmer.config = config
        return trimmer
    
    @staticmethod
    def createDefaultConfig():
        """创建默认配置"""
        return TrimConfig()

class TrimValidator:
    """裁剪验证器"""
    @staticmethod
    def validateInputPath(inputPath):
        """验证输入路径"""
        if not inputPath or not os.path.exists(inputPath):
            raise ValueError("Invalid input path")
        return True
    
    @staticmethod
    def validateOutputPath(outputPath):
        """验证输出路径"""
        if not outputPath:
            raise ValueError("Output path is required")
        return True
    
    @staticmethod
    def validateTimeValue(time):
        """验证时间值"""
        if time < 0:
            raise ValueError("Time cannot be negative")
        return True