from pytube import YouTube
import ffmpeg
from moviepy.editor import VideoFileClip, AudioFileClip
import re
import subprocess

COMPLETE_PATH = './complete'
INCOMPLETE_PATH = './incomplete'

# YouTube objektum létrehozása
YOUTUBE_URL = 'https://www.youtube.com/watch?v=taJ5pN7Zdn0'
yt = YouTube(YOUTUBE_URL)
video_title = yt.title


class FileName:
    def __init__(self, video_title):
        self.filename = self.create_filename(video_title)
        self.filename_video = f"{self.filename}_video.mp4"
        self.filename_audio = f"{self.filename}_audio.mp4"

    def create_filename(self, text, max_words=4):
        # Speciális karakterek eltávolítása
        text = re.sub(r'[^\w\s]', '', text)
        # Első max_words számú szó kiválasztása
        words = text.split()[:max_words]
        # Szavak összekapcsolása alulvonással
        _filename = '_'.join(words)
        return _filename


def download_video():
    available_resolutions = []
    try:
        streams = yt.streams.filter(only_video=True)
        for stream in streams:
            available_resolutions.append(stream.resolution)

        resolution = ''
        if "1080p" in available_resolutions:
            print(f"1080p elérhető")
            resolution = "1080p"
        elif "1080p50" in available_resolutions:
            print(f"1080p50 elérhető")
            resolution = "1080p50"
        elif "720p" in available_resolutions:
            print(f"720p elérhető")
            resolution = "720p"
        else:
            print("Nincs megfelelő formátum")
            exit()

        stream = yt.streams.filter(res=resolution, file_extension="mp4").first()

        if stream:
            print(f"Videó letöltés indítása: \n{video_title}")
            stream.download(INCOMPLETE_PATH, filename=f"{filenames.filename_video}")
            print(f"Videó befejezve, fájlnév: {filenames.filename_video}")

        else:
            print("Az 1080p felbontású videó nem érhető el ebben a formátumban.")

    except Exception as e:
        print(f"Hiba történt a letöltés során: {str(e)}")


def download_audio():
    try:
        # Legjobb minőségű audio stream kiválasztása
        audio_stream = yt.streams.filter(only_audio=True).first()

        if audio_stream:
            # Letöltés indítása
            print(f"Hang letöltése indítása: {video_title}")
            audio_stream.download(INCOMPLETE_PATH, filename=f"{filenames.filename_audio}")
            print(f"Hang letöltés befejezve:")

        else:
            print("Nem találtunk elérhető audio stream-et.")

    except Exception as e:
        print(f"Hiba történt a letöltés során: {str(e)}")


def merge_video_audio_pymovie():
    try:
        # Videó betöltése
        video_clip = VideoFileClip(f'{INCOMPLETE_PATH}/{filenames.filename_video}')

        # Audió betöltése
        audio_clip = AudioFileClip(f'{INCOMPLETE_PATH}/{filenames.filename_audio}')

        # Audió hozzáadása a videóhoz
        video_with_audio = video_clip.set_audio(audio_clip)

        # Egyesített fájl mentése
        video_with_audio.write_videofile(f'{COMPLETE_PATH}/{filenames.filename}.mp4', codec="libx264", audio_codec="aac")

        print(f"A fájlok egyesítése sikeres: {filenames.filename}.mp4")

    except Exception as e:
        print(f"Hiba történt a fájlok egyesítése során: {str(e)}")


def merge_video_audio_ffmpeg_python():
    try:
        # FFmpeg segítségével a videó és audió fájlok egyesítése
        input_video = ffmpeg.input(f'{INCOMPLETE_PATH}/{filenames.filename_video}')
        input_audio = ffmpeg.input(f'{INCOMPLETE_PATH}/{filenames.filename_audio}')
        output_file = f"{COMPLETE_PATH}/{filenames.filename}.mp4"

        # Videó és audió kombinálása és mentése
        ffmpeg.output(input_video, input_audio, output_file).run(overwrite_output=True)

        print(f"A fájlok egyesítése sikeres: {output_file}")
    except ffmpeg.Error as e:
        print(f"Hiba történt a fájlok egyesítése során: {e.stderr.decode('utf-8')}")


def merge_video_audio(video_file, audio_file, output_file):
    try:
        # FFmpeg parancs futtatása a subprocess modullal
        command = [
            'ffmpeg', '-i', f'{INCOMPLETE_PATH}/{filenames.filename_video}', '-i', f'{INCOMPLETE_PATH}/{filenames.filename_audio}',
            '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', f"{COMPLETE_PATH}/{filenames.filename}.mp4"
        ]

        # Futtatja az FFmpeg parancsot
        subprocess.run(command, check=True)
        print(f"A fájlok egyesítése sikeres: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Hiba történt a fájlok egyesítése során: {e}")


if __name__ == "__main__":
    filenames = FileName(video_title)
    # download_video()
    # download_audio()

    # MERGE
    # merge_video_audio_ffmpeg_python()
    merge_video_audio_pymovie()
