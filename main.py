from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip
import re
from pathlib import Path
import shutil


class FileName:
    def __init__(self, _video_title):
        self.filename = self.create_filename(_video_title)
        self.filename_video = f"{self.filename}_video.mp4"
        self.filename_audio = f"{self.filename}_audio.mp4"

    @staticmethod
    def create_filename(text, max_words=4):
        # Remove special characters
        text = re.sub(r'[^\w\s]', '', text)
        # First max_words finding
        words = text.split()[:max_words]
        # Merge words with underlines
        _filename = '_'.join(words)

        return _filename


def read_urls_from_file():
    _urls = []
    with open('download_list.txt', 'r') as file:
        _urls = [line.strip() for line in file.readlines()]

    return _urls


def download_video():
    available_resolutions = []
    try:
        streams = yt.streams.filter(only_video=True)
        for video_stream in streams:
            available_resolutions.append(video_stream.resolution)

        resolution = ''
        if "1080p" in available_resolutions:
            print(f"1080p available")
            resolution = "1080p"
        elif "1080p50" in available_resolutions:
            print(f"1080p50 available")
            resolution = "1080p50"
        elif "720p" in available_resolutions:
            print(f"720p available")
            resolution = "720p"
        elif "720p50" in available_resolutions:
            print(f"720p50 available")
            resolution = "720p50"
        else:
            print("High quality resolution is not available")
            exit()

        video_stream = yt.streams.filter(res=resolution, file_extension="mp4").first()

        if video_stream:
            print(f"Video downloading...")
            video_stream.download(INCOMPLETE_PATH, filename=f"{filenames.filename_video}")
            print(f"Video done")

    except Exception as e:
        print(f"ERROR with video download: {str(e)}")


def download_audio():
    try:
        audio_stream = yt.streams.filter(only_audio=True).first()

        if audio_stream:
            print(f"Audio downloading...")
            audio_stream.download(INCOMPLETE_PATH, filename=f"{filenames.filename_audio}")
            print(f"Audio done")

        else:
            print("No available audio")

    except Exception as e:
        print(f"ERROR with audio download: {str(e)}")


def merge_video_audio():
    try:
        # Loading video
        video_clip = VideoFileClip(f'{INCOMPLETE_PATH}/{filenames.filename_video}')

        # Loadin video
        audio_clip = AudioFileClip(f'{INCOMPLETE_PATH}/{filenames.filename_audio}')

        # Add audio to video
        video_with_audio = video_clip.set_audio(audio_clip)

        # Save merged file
        video_with_audio.write_videofile(f'{COMPLETE_PATH}/{filenames.filename}.mp4', codec="libx264", audio_codec="aac")

        print(f"File merging success : {filenames.filename}.mp4")

    except Exception as e:
        print(f"ERROR with merging: {str(e)}")


if __name__ == "__main__":
    print(f'1. I want add an URL\n2. I added URLs to txt\n{"-" * 40}')
    menu = input('Add your number:')
    print(f'Your menu number: {menu}')

    # Directories
    dir_path_incomplete = Path("incomplete")
    dir_path_incomplete.mkdir(exist_ok=True)
    dir_path_complete = Path("complete")
    dir_path_complete.mkdir(exist_ok=True)
    print(f"Directory created: {dir_path_incomplete}")

    COMPLETE_PATH = './complete'
    INCOMPLETE_PATH = './incomplete'

    urls = read_urls_from_file()

    for url in urls:
        # CREATE YT OBJECT
        yt = YouTube(url)
        video_title = yt.title
        print(f"\n{video_title}\n{'-' * len(video_title)}")

        # FORMAT FILENAME
        filenames = FileName(video_title)

        # DOWNLOAD
        download_video()
        download_audio()

        # MERGE
        merge_video_audio()

    # REMOVE TEMPORARY DIR
    shutil.rmtree(dir_path_incomplete)
    print(f"Remove temporary dir: {dir_path_incomplete}")
