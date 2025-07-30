import subprocess
import json
from .setup import getFFmpegPath

class MetadataReader:
    def readMetadata(self, video_path):
        ffmpeg = getFFmpegPath()
        result = subprocess.run([ffmpeg, '-i', video_path, '-f', 'ffmetadata', '-'], capture_output=True, text=True)
        return result.stderr

class MetadataWriter:
    def writeMetadata(self, input_path, output_path, metadata_dict):
        ffmpeg = getFFmpegPath()
        with open('metadata.txt', 'w') as f:
            for key, value in metadata_dict.items():
                f.write(f"{key}={value}\n")
        subprocess.run([ffmpeg, '-i', input_path, '-i', 'metadata.txt', 
                       '-map_metadata', '1', '-codec', 'copy', output_path])

class ChapterAdder:
    def addChapters(self, input_path, chapters, output_path):
        ffmpeg = getFFmpegPath()
        metadata = ";FFMETADATA1\n"
        for i, (start, end, title) in enumerate(chapters):
            metadata += f"[CHAPTER]\nSTART={start}\nEND={end}\ntitle={title}\n\n"
        
        with open('chapters.txt', 'w') as f:
            f.write(metadata)
            
        subprocess.run([ffmpeg, '-i', input_path, '-i', 'chapters.txt', 
                       '-map_metadata', '1', '-codec', 'copy', output_path])

class GPSDataHandler:
    def addGPSData(self, input_path, output_path, lat, lon):
        ffmpeg = getFFmpegPath()
        subprocess.run([ffmpeg, '-i', input_path, 
                       '-metadata', f'location={lat}+{lon}', 
                       '-metadata', 'location-eng=My Location', 
                       '-codec', 'copy', output_path])

class CreationTimeSetter:
    def setCreationTime(self, input_path, output_path, creation_time):
        ffmpeg = getFFmpegPath()
        subprocess.run([ffmpeg, '-i', input_path, 
                       '-metadata', f'creation_time={creation_time}', 
                       '-codec', 'copy', output_path])

class ThumbnailEmbedder:
    def embedThumbnail(self, video_path, image_path, output_path):
        ffmpeg = getFFmpegPath()
        subprocess.run([ffmpeg, '-i', video_path, '-i', image_path, 
                       '-map', '0', '-map', '1', '-c', 'copy', '-disposition:v:1', 'attached_pic', 
                       output_path])

# 独立函数
def removeAllMetadata(input_path, output_path):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-map_metadata', '-1', output_path])

def changeTitle(input_path, output_path, title):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-metadata', f'title={title}', '-codec', 'copy', output_path])

def changeAuthor(input_path, output_path, author):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-metadata', f'author={author}', '-codec', 'copy', output_path])

def changeAlbum(input_path, output_path, album):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-metadata', f'album={album}', '-codec', 'copy', output_path])

def changeYear(input_path, output_path, year):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-metadata', f'date={year}', '-codec', 'copy', output_path])

def addComment(input_path, output_path, comment):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-metadata', f'comment={comment}', '-codec', 'copy', output_path])

def addCopyright(input_path, output_path, copyright_text):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-metadata', f'copyright={copyright_text}', '-codec', 'copy', output_path])

def setLanguage(input_path, output_path, language):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-metadata:s:a:0', f'language={language}', '-codec', 'copy', output_path])

def extractMetadataToFile(input_path, output_file):
    ffmpeg = getFFmpegPath()
    subprocess.run([ffmpeg, '-i', input_path, '-f', 'ffmetadata', output_file])