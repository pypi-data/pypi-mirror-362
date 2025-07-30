import os
import sys
import subprocess
import zipfile
from pathlib import Path

class FfmpegManager:
    """管理FFmpeg的提取和执行"""
    def __init__(self):
        # 获取项目根目录（audio目录的父目录）
        self.baseDir = Path(__file__).parent.parent
        self.ffmpegZipPath = self.baseDir / "ffmpeg.zip"
        self.ffmpegDir = self.baseDir / "ffmpeg"
        self.ffmpegExePath = self.ffmpegDir / "ffmpeg" / "bin" / "ffmpeg.exe"
        
    def extractFfmpeg(self):
        """从ZIP文件中提取FFmpeg"""
        if not self.ffmpegZipPath.exists():
            raise FileNotFoundError(f"FFmpeg ZIP file not found at {self.ffmpegZipPath}")
        
        if not self.ffmpegExePath.exists():
            with zipfile.ZipFile(self.ffmpegZipPath, 'r') as zipRef:
                zipRef.extractall(self.ffmpegDir)
            print("FFmpeg extracted successfully")
    
    def getFfmpegPath(self):
        """获取FFmpeg可执行文件路径"""
        if not self.ffmpegExePath.exists():
            self.extractFfmpeg()
        return str(self.ffmpegExePath)

class AudioProcessorBase:
    """音频处理基类"""
    def __init__(self):
        self.ffmpegManager = FfmpegManager()
        self.ffmpegPath = self.ffmpegManager.getFfmpegPath()
    
    def runFfmpegCommand(self, command):
        """执行FFmpeg命令"""
        fullCmd = [self.ffmpegPath] + command
        try:
            result = subprocess.run(
                fullCmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg error: {e.stderr}") from e
    
    def validateInputFile(self, filePath):
        """验证输入文件是否存在"""
        if not Path(filePath).exists():
            raise FileNotFoundError(f"Input file not found: {filePath}")
        return True
    
    def validateOutputPath(self, outputPath):
        """验证输出路径是否有效"""
        outputDir = Path(outputPath).parent
        if not outputDir.exists():
            os.makedirs(outputDir)
        return True
    
    def getFileMetadata(self, filePath):
        """获取文件元数据"""
        command = ["-i", filePath]
        try:
            self.runFfmpegCommand(command)
        except RuntimeError as e:
            # 元数据通常在错误输出中
            return str(e)
        return ""
    
    def normalizePath(self, path):
        """规范化路径"""
        return str(Path(path).absolute())
    
    def formatTime(self, seconds):
        """将秒数格式化为HH:MM:SS.ms"""
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{seconds:06.3f}"
    
    def parseTime(self, timeStr):
        """将时间字符串解析为秒数"""
        parts = timeStr.split(':')
        if len(parts) == 3:
            return float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
        elif len(parts) == 2:
            return float(parts[0])*60 + float(parts[1])
        return float(timeStr)
    
    def isAudioFile(self, filePath):
        """检查文件是否为音频文件"""
        metadata = self.getFileMetadata(filePath)
        return "Audio" in metadata

class AudioTrimInterface:
    """音频裁剪接口"""
    def trimAudio(self, inputPath, outputPath, startTime, duration):
        pass
    
    def trimToEnd(self, inputPath, outputPath, startTime):
        pass
    
    def trimSilence(self, inputPath, outputPath, threshold=-30):
        pass

class AudioMergeInterface:
    """音频合并接口"""
    def mergeFiles(self, inputFiles, outputPath):
        pass
    
    def mergeWithCrossfade(self, inputFiles, outputPath, fadeDuration=1.0):
        pass

class AudioConvertInterface:
    """音频转换接口"""
    def convertFormat(self, inputPath, outputPath, codec="libmp3lame", bitrate="192k"):
        pass
    
    def changeSampleRate(self, inputPath, outputPath, sampleRate=44100):
        pass
    
    def changeChannels(self, inputPath, outputPath, channels=2):
        pass

class AudioExtractInterface:
    """音频提取接口"""
    def extractFromVideo(self, videoPath, outputPath):
        pass
    
    def extractMultipleTracks(self, videoPath, outputPattern, trackIndices=[0]):
        pass

# 导入数据模块
from .data.trim import AudioTrimmer
from .data.merge import AudioMerger
from .data.convert import AudioConverter
from .data.extract import AudioExtractor

# 创建实例供外部使用
audioTrimmer = AudioTrimmer()
audioMerger = AudioMerger()
audioConverter = AudioConverter()
audioExtractor = AudioExtractor()