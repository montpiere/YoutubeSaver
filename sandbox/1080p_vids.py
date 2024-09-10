from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip
import os

VIDEO_PATH = './movies'
AUDIO_PATH = './audio'
COMPLETE_PATH = './complete'

# YouTube objektum létrehozása
YOUTUBE_URL = 'https://www.youtube.com/watch?v=dcHbg3-dxis'
yt = YouTube(YOUTUBE_URL)
TITLE = yt.title

video_streams = yt.streams.filter(only_video=True)
for stream in video_streams:
    print(f"{stream.resolution} - {stream.mime_type} - {stream.filesize // (1024 * 1024)} MB")


def download_1080p_video():
    try:
        # 1080p felbontású videó stream kiválasztása
        stream = yt.streams.filter(res="1080p", file_extension="mp4").first()

        if stream:
            # Letöltés indítása
            print(f"Videó letöltés indítása: {TITLE}")
            stream.download(VIDEO_PATH)
            print(f"Videó befejezve: {TITLE}")

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
            print(f"Hang letöltése indítása: {TITLE}")
            audio_stream.download(AUDIO_PATH)
            print(f"Hang letöltés befejezve:")

        else:
            print("Nem találtunk elérhető audio stream-et.")

    except Exception as e:
        print(f"Hiba történt a letöltés során: {str(e)}")


def download_caption(url, output_path='./caption'):
    lang = 'en'
    try:
        # YouTube objektum létrehozása
        yt = YouTube(url)

        # Elérhető feliratok listázása
        captions = yt.captions

        # Ellenőrizni, hogy elérhető-e a kívánt nyelvű felirat
        if lang in captions:
            caption = captions[lang]
            # A felirat letöltése SRT formátumban
            srt_captions = caption.generate_srt_captions()

            # Felirat fájl mentése
            file_name = f"{yt.title}_{lang}.srt"
            file_path = f"{output_path}/{file_name}"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(srt_captions)

            print(f"Felirat letöltése befejezve: {file_name}")
        else:
            print(f"Nincs elérhető felirat a '{lang}' nyelven.")
    except Exception as e:
        print(f"Hiba történt a felirat letöltése során: {str(e)}")


def list_available_captions(url):
    try:
        # YouTube objektum létrehozása
        yt = YouTube(url)

        # Elérhető feliratok listázása
        captions = yt.captions

        if captions:
            print("Elérhető feliratok:")
            for caption in captions:
                print(f"Nyelvkód: {caption.code}, Nyelv: {caption.name}")
        else:
            print("Nem érhető el felirat ehhez a videóhoz.")
    except Exception as e:
        print(f"Hiba történt a feliratok lekérdezése során: {str(e)}")


def merge_video_audio():
    try:
        # Videó betöltése
        video_clip = VideoFileClip(f'{VIDEO_PATH}/{TITLE}.mp4')

        # Audió betöltése
        audio_clip = AudioFileClip(f'{AUDIO_PATH}/{TITLE}.mp4')

        # Audió hozzáadása a videóhoz
        video_with_audio = video_clip.set_audio(audio_clip)

        # Egyesített fájl mentése
        video_with_audio.write_videofile(f'{COMPLETE_PATH}/{TITLE}.mp4', codec="libx264", audio_codec="aac")

        print(f"A fájlok egyesítése sikeres: {TITLE}.mp4")
    except Exception as e:
        print(f"Hiba történt a fájlok egyesítése során: {str(e)}")


if __name__ == "__main__":
    download_1080p_video()
    download_audio()
    merge_video_audio()
    # download_caption(video_url, download_path)
    # list_available_captions(video_url)



