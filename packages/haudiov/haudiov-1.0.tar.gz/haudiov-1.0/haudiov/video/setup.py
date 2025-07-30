import os
import zipfile
import sys
from pathlib import Path

def extractFFmpeg():
    baseDir = Path(__file__).parent.parent
    zip_path = baseDir / "ffmpeg.zip"
    extract_dir = baseDir / "ffmpeg"
    
    if not os.path.exists(zip_path):
        print(f"错误: 未找到 {zip_path}")
        sys.exit(1)
        
    if not os.path.exists(extract_dir):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

def getFFmpegPath():
    return os.path.join(Path(__file__).parent.parent,"ffmpeg", "bin", "ffmpeg.exe")

if __name__ == "__main__":
    extractFFmpeg()
    print("FFmpeg 路径:", getFFmpegPath())