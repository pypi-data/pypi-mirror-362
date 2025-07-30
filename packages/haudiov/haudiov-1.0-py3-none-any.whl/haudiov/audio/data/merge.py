from .. import AudioProcessorBase, AudioMergeInterface
import os, re
import tempfile

class MergeConfig:
    """合并配置类"""
    def __init__(self):
        self.crossfadeDuration = 1.0
        self.outputFormat = "mp3"
        self.bitrate = "192k"
        self.normalize = True
        self.deleteTempFiles = True

class MergeResult:
    """合并结果类"""
    def __init__(self, success, outputPath, fileCount, duration, message=""):
        self.success = success
        self.outputPath = outputPath
        self.fileCount = fileCount
        self.duration = duration
        self.message = message
    
    def __str__(self):
        return f"Merged {self.fileCount} files to {self.outputPath}"

class MergeProgress:
    """合并进度类"""
    def __init__(self):
        self.currentFile = 0
        self.totalFiles = 0
        self.percentage = 0
    
    def update(self, currentFile, totalFiles):
        """更新进度"""
        self.currentFile = currentFile
        self.totalFiles = totalFiles
        self.percentage = (currentFile / totalFiles) * 100 if totalFiles > 0 else 0

class MergeError(Exception):
    """合并错误异常类"""
    def __init__(self, message, errorCode):
        super().__init__(message)
        self.errorCode = errorCode

class AudioMerger(AudioProcessorBase, AudioMergeInterface):
    """音频合并器"""
    def __init__(self):
        super().__init__()
        self.config = MergeConfig()
    
    def mergeFiles(self, inputFiles, outputPath):
        """合并多个音频文件"""
        self.validateInputFiles(inputFiles)
        self.validateOutputPath(outputPath)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=self.config.deleteTempFiles) as tempFile:
            for file in inputFiles:
                absPath = os.path.abspath(file)
                tempFile.write(f"file '{absPath}'\n")
            tempFile.flush()
            
            command = [
                "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", tempFile.name,
                "-c", "copy",
                outputPath
            ]
            
            try:
                self.runFfmpegCommand(command)
                return MergeResult(True, outputPath, len(inputFiles), 0, "Merge completed")
            except Exception as e:
                return MergeResult(False, outputPath, len(inputFiles), 0, str(e))
    
    def mergeWithCrossfade(self, inputFiles, outputPath, fadeDuration=1.0):
        """带交叉淡入淡出效果的合并"""
        self.validateInputFiles(inputFiles)
        self.validateOutputPath(outputPath)
        
        if len(inputFiles) < 2:
            raise MergeError("At least two files required for crossfade", 2001)
        
        tempFiles = []
        try:
            # 为每个文件创建淡入淡出版本
            for i, file in enumerate(inputFiles):
                tempPath = os.path.join(tempfile.gettempdir(), f"temp_{i}.{self.config.outputFormat}")
                tempFiles.append(tempPath)
                
                # 应用淡入淡出效果
                self.applyCrossfade(file, tempPath, 
                                   fadeIn=(i == 0), 
                                   fadeOut=(i == len(inputFiles)-1),
                                   fadeDuration=fadeDuration)
            
            # 合并处理后的文件
            return self.mergeFiles(tempFiles, outputPath)
        finally:
            if self.config.deleteTempFiles:
                for file in tempFiles:
                    if os.path.exists(file):
                        os.remove(file)
    
    def applyCrossfade(self, inputPath, outputPath, fadeIn=True, fadeOut=True, fadeDuration=1.0):
        """应用交叉淡入淡出效果"""
        command = ["-y", "-i", inputPath]
        
        filters = []
        if fadeIn:
            filters.append(f"afade=t=in:d={fadeDuration}")
        if fadeOut:
            filters.append(f"afade=t=out:st=0:d={fadeDuration}")
        
        if filters:
            command += ["-af", ",".join(filters)]
        
        command.append(outputPath)
        
        try:
            self.runFfmpegCommand(command)
            return True
        except Exception as e:
            raise MergeError(f"Crossfade failed: {str(e)}", 2002)
    
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
            raise MergeError(f"Normalization failed: {str(e)}", 2003)
    
    def concatWithTranscode(self, inputFiles, outputPath):
        """转码后连接文件"""
        self.validateInputFiles(inputFiles)
        self.validateOutputPath(outputPath)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=self.config.deleteTempFiles) as tempFile:
            for file in inputFiles:
                absPath = os.path.abspath(file)
                tempFile.write(f"file '{absPath}'\n")
            tempFile.flush()
            
            command = [
                "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", tempFile.name,
                "-c:a", "libmp3lame",
                "-b:a", self.config.bitrate,
                outputPath
            ]
            
            try:
                self.runFfmpegCommand(command)
                return MergeResult(True, outputPath, len(inputFiles), 0, "Transcoded merge completed")
            except Exception as e:
                return MergeResult(False, outputPath, len(inputFiles), 0, str(e))
    
    def mixAudios(self, inputFiles, outputPath):
        """混合多个音频文件"""
        if len(inputFiles) < 2:
            raise MergeError("At least two files required for mixing", 2004)
        
        inputs = []
        filterComplex = []
        for i, file in enumerate(inputFiles):
            inputs.extend(["-i", file])
            filterComplex.append(f"[{i}:a]")
        
        filterComplex = "".join(filterComplex) + f"amix=inputs={len(inputFiles)}:duration=longest[a]"
        
        command = [
            "-y"
        ] + inputs + [
            "-filter_complex", filterComplex,
            "-map", "[a]",
            outputPath
        ]
        
        try:
            self.runFfmpegCommand(command)
            return MergeResult(True, outputPath, len(inputFiles), 0, "Audio mixing completed")
        except Exception as e:
            return MergeResult(False, outputPath, len(inputFiles), 0, str(e))
    
    def mergeToVideo(self, videoPath, audioPath, outputPath):
        """将音频合并到视频"""
        self.validateInputFile(videoPath)
        self.validateInputFile(audioPath)
        self.validateOutputPath(outputPath)
        
        command = [
            "-y",
            "-i", videoPath,
            "-i", audioPath,
            "-c:v", "copy",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            outputPath
        ]
        
        try:
            self.runFfmpegCommand(command)
            return True
        except Exception as e:
            raise MergeError(f"Merge to video failed: {str(e)}", 2005)
    
    def validateInputFiles(self, inputFiles):
        """验证输入文件列表"""
        if not inputFiles or len(inputFiles) == 0:
            raise ValueError("No input files provided")
        
        for file in inputFiles:
            self.validateInputFile(file)
        
        return True
    
    def setOutputFormat(self, format):
        """设置输出格式"""
        self.config.outputFormat = format
    
    def setBitrate(self, bitrate):
        """设置比特率"""
        self.config.bitrate = bitrate
    
    def setNormalization(self, normalize):
        """设置是否标准化"""
        self.config.normalize = normalize

class MergeUtils:
    """合并工具类"""
    @staticmethod
    def generateOutputPath(inputFiles, extension="mp3"):
        """生成输出路径"""
        baseName = os.path.splitext(os.path.basename(inputFiles[0]))[0]
        return f"{baseName}_merged.{extension}"
    
    @staticmethod
    def validateFileList(fileList):
        """验证文件列表"""
        if not isinstance(fileList, list):
            raise TypeError("Input must be a list")
        return True
    
    @staticmethod
    def getTotalDuration(fileList):
        """获取音频文件列表的总持续时间（完整版）"""
        from .. import AudioProcessorBase
        processor = AudioProcessorBase()
        total_duration = 0.0
        
        for file_path in fileList:
            try:
                # 获取元数据
                metadata = processor.getFileMetadata(file_path)
                
                # 从元数据中解析持续时间
                duration_match = re.search(
                    r'Duration:\s(\d+):(\d+):(\d+\.\d+)', 
                    metadata
                )
                
                if duration_match:
                    hours = int(duration_match.group(1))
                    minutes = int(duration_match.group(2))
                    seconds = float(duration_match.group(3))
                    duration_sec = hours * 3600 + minutes * 60 + seconds
                    total_duration += duration_sec
            except Exception:
                # 错误处理：使用默认值30秒
                total_duration += 30.0
        
        return total_duration
    
    @staticmethod
    def createTempFileList(fileList):
        """创建临时文件列表"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tempFile:
            for file in fileList:
                tempFile.write(f"file '{file}'\n")
            return tempFile.name

class MergeFactory:
    """合并工厂类"""
    @staticmethod
    def createMerger(config=None):
        """创建合并器实例"""
        merger = AudioMerger()
        if config:
            merger.config = config
        return merger
    
    @staticmethod
    def createDefaultConfig():
        """创建默认配置"""
        return MergeConfig()

class MergeValidator:
    """合并验证器"""
    @staticmethod
    def validateFilePaths(filePaths):
        """验证文件路径列表"""
        if not filePaths or len(filePaths) == 0:
            raise ValueError("File list is empty")
        
        for path in filePaths:
            if not os.path.exists(path):
                raise FileNotFoundError(f"File not found: {path}")
        return True
    
    @staticmethod
    def validateCrossfadeDuration(duration):
        """验证交叉淡入淡出持续时间"""
        if duration <= 0:
            raise ValueError("Crossfade duration must be positive")
        return True