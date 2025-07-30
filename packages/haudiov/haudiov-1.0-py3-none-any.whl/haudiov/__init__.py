__version__ = "1.0"

from . import audio
from . import video
from pathlib import Path
import subprocess
import time
import os, sys, zipfile
import threading
import pyaudio
from pyfiglet import Figlet

def extractFFmpeg():
    zip_path = Path(__file__).parent / "ffmpeg.zip"
    extract_dir = Path(__file__).parent / "ffmpeg"
    
    if not os.path.exists(zip_path):
        print(f"错误: 未找到 {zip_path}")
        sys.exit(1)
        
    if not os.path.exists(extract_dir):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

def getFFmpegPath():
    return os.path.join(Path(__file__).parent,"ffmpeg", "bin", "ffmpeg.exe")

def VideoAudioCombine(video_path, audio_path, output_path, 
                     video_codec='copy', audio_codec='aac'):
    """
    将视频文件和音频文件合并为新的视频文件
    
    参数:
    video_path (str): 原始视频文件路径
    audio_path (str): 要添加的音频文件路径
    output_path (str): 输出文件路径
    video_codec (str): 视频编码器 (默认: 'copy' 表示不重新编码)
    audio_codec (str): 音频编码器 (默认: 'aac')
    """
    extractFFmpeg()
    ffmpeg = getFFmpegPath()
    
    # 构建FFmpeg命令
    cmd = [
        ffmpeg,
        '-i', video_path,    # 输入视频
        '-i', audio_path,    # 输入音频
        '-c:v', video_codec, # 视频编码设置
        '-c:a', audio_codec, # 音频编码设置
        '-map', '0:v:0',     # 使用第一个输入文件的视频流
        '-map', '1:a:0',     # 使用第二个输入文件的音频流
        '-shortest',         # 以最短的输入流结束
        '-y',                # 覆盖输出文件
        output_path,
    ]

    # 执行命令
    subprocess.run(cmd, check=True)



class PlayMusic:
    def __init__(self):
        extractFFmpeg()
        self.ffmpeg_path = Path(__file__).parent
        self._p = pyaudio.PyAudio()
        self._playing = False
        self._thread = None
        self._stop_event = threading.Event()
    
    def play(self, file_path, duration=-0):
        """播放音乐文件
        
        Args:
            file_path: 音乐文件路径
            duration: 播放时长
                -1: 无限循环播放
                -0: 播放完整文件后停止
                >0: 播放指定秒数
        """
        # 停止当前播放
        self.stop()
        
        # 重置停止事件
        self._stop_event.clear()
        self._playing = True
        
        # 创建播放线程
        self._thread = threading.Thread(
            target=self._play_thread, 
            args=(file_path, duration),
            daemon=True
        )
        self._thread.start()
    
    def stop(self):
        """停止播放"""
        if not self._playing:
            return
        
        self._stop_event.set()
        self._playing = False
        
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)
        
        self._thread = None
    
    def _play_thread(self, file_path, duration):
        """播放线程"""
        # 创建临时PCM文件路径
        temp_file = "temp_music.pcm"
        
        # 无限循环处理
        loop_count = 1
        if duration == -1:
            loop_count = -1  # 无限循环
        
        # 音频参数
        sample_rate = 44100
        channels = 2
        sample_width = 2  # 16-bit = 2 bytes
        
        try:
            while loop_count != 0 and not self._stop_event.is_set():
                # 构建FFmpeg命令
                cmd = [
                    self.ffmpeg_path,
                    '-i', file_path,
                    '-f', 's16le',       # PCM格式
                    '-acodec', 'pcm_s16le',
                    '-ar', str(sample_rate),
                    '-ac', str(channels),
                    '-y',                # 覆盖输出文件
                ]
                
                # 添加时长限制
                if duration > 0:
                    cmd.extend(['-t', str(duration)])
                
                cmd.append(temp_file)
                
                # 运行FFmpeg转换
                subprocess.run(
                    cmd, 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True
                )
                
                # 播放PCM数据
                self._play_pcm(temp_file, sample_rate, channels, sample_width)
                
                # 清理临时文件
                try:
                    os.remove(temp_file)
                except:
                    pass
                
                # 更新循环计数
                if loop_count > 0:
                    loop_count -= 1
        
        except Exception as e:
            print(f"播放错误: {e}")
        finally:
            self._playing = False
            # 确保清理临时文件
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
    
    def _play_pcm(self, file_path, sample_rate, channels, sample_width):
        """播放PCM音频数据"""
        chunk = 4096  # 每次读取的块大小
        
        # 打开PCM文件
        with open(file_path, 'rb') as pcm_file:
            # 打开音频流
            stream = self._p.open(
                format=self._p.get_format_from_width(sample_width),
                channels=channels,
                rate=sample_rate,
                output=True
            )
            
            # 播放音频
            data = pcm_file.read(chunk)
            while data and not self._stop_event.is_set():
                stream.write(data)
                data = pcm_file.read(chunk)
            
            # 停止流
            stream.stop_stream()
            stream.close()
    
    def __del__(self):
        self.stop()
        self._p.terminate()


# test
def default(font:str ="larry3d",text: str = "pyfiglet", width: int =200) -> str: 
    f = Figlet(font=font, width=width)
    return f.renderText(text)

__all__ = ["VideoAudioCombine","video","audio","PlayMusic"]