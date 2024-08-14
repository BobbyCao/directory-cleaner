import os
import shutil

import time
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# * source_dir is the folder being tracked
source_dir = "C:\\Users\\bob1\\Desktop"

# * destination directories for files
audio_dir = "C:\\Users\\bob1\\Desktop\\music"
video_dir = "C:\\Users\\bob1\\Desktop\\videos"
image_dir = "C:\\Users\\bob1\\Desktop\\images"
document_dir = "C:\\Users\\bob1\\Desktop\\docs"
misc_dir = "C:\\Users\\bob1\\Desktop\\misc"

# * Below are supported file extension names
# * images, videos, audio, and document types supported
image_extensions = ['.JPG', '.JPEG', '.JPE', '.JIF', '.JFIF', '.JFI', '.PNG', '.GIF', '.WEBP', '.TIFF', '.TIF', '.PSD',
                  '.RAW', '.ARW', '.CR2', '.NRW', '.K25', '.BMP', '.DIB', '.HEIF', '.HEIC', '.IND', '.INDD', '.INDT',
                  '.JP2', '.J2K', '.JPF', '.JPF', '.JPX', '.JPM', '.MJ2', '.SVG', '.SVGZ', '.AI', '.EPS', '.ICO']

video_extensions = ['.WEBM', '.MPG', '.MP2', '.MPEG', '.MPE', '.MPV', '.OGG', '.MP4', '.MP4V',
                  '.M4V', '.AVI', '.WMV', '.MOV', '.QT', '.FLV', '.SWF', '.AVCHD']

audio_extensions = ['.M4A', '.FLAC', 'MP3', '.WAV', '.WMA', '.AAC']

document_extensions = ['.DOC', '.DOCX', '.ODT', '.PDF', '.XLS', '.XLSX', '.PPT', '.PPTX']


def make_unique(dest, name):
    fileName, extension = os.path.splitext(name)
    counter = 1
    
    while os.path.exists(f"{dest}\\{name}"):
        name = f"{fileName}({str(counter)}){extension}"
        counter += 1

    return name

def move_file(dest, entry, fileName):
    if os.path.exists(f"{dest}\\{fileName}"):
        uniqueName = make_unique(dest, fileName)
        oldName = os.path.join(dest, fileName)
        newName = os.path.join(dest, uniqueName)
        os.rename(oldName, newName)
    shutil.move(entry, dest)

class FileMover(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)
    
    def check_audio_files(self, entry, name):
        for audio_extension in audio_extensions:
            if name.upper().endswith(audio_extension):
                move_file(audio_dir, entry, name)
                logging.info(f"Moved file: {name}")

    def check_video_files(self, entry, name):
        for video_extension in video_extensions:
            if name.upper().endswith(video_extension):
                move_file(video_dir, entry, name)
                logging.info(f"Moved file: {name}")

    def check_image_files(self, entry, name):
        for image_extension in image_extensions:
            if name.upper().endswith(image_extension):
                move_file(image_dir, entry, name)
                logging.info(f"Moved file: {name}")

    def check_document_files(self, entry, name):
        for document_extension in document_extensions:
            if name.upper().endswith(document_extension):
                move_file(document_dir, entry, name)
                logging.info(f"Moved file: {name}")



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = FileMover()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
