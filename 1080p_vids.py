from pytube import YouTube
import os


def download_1080p_video(url, output_path='.'):
    try:
        # YouTube objektum létrehozása
        yt = YouTube(url)

        # 1080p felbontású videó stream kiválasztása
        stream = yt.streams.filter(res="1080p", file_extension="mp4").first()

        if stream:
            # Letöltés indítása
            print(f"Videó letöltés indítása: {yt.title}")
            # stream.download(output_path)
            stream.download('./movies')
            print(f"Videó befejezve: {yt.title}")
        else:
            print("Az 1080p felbontású videó nem érhető el ebben a formátumban.")
    except Exception as e:
        print(f"Hiba történt a letöltés során: {str(e)}")


def download_audio(url, output_path='.'):
    try:
        # YouTube objektum létrehozása
        yt = YouTube(url)

        # Legjobb minőségű audio stream kiválasztása
        audio_stream = yt.streams.filter(only_audio=True).first()

        if audio_stream:
            # Letöltés indítása
            print(f"Hang letöltése indítása: {yt.title}")
            # audio_stream.download(output_path)
            audio_stream.download('./audio')

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


if __name__ == "__main__":
    video_url = 'https://www.youtube.com/watch?v=0Co1Iptd4p4'
    download_path = './movies'
    print('Letöltés indítása...')
    # download_1080p_video(video_url, download_path)
    # download_audio(video_url, download_path)
    # download_caption(video_url, download_path)
    list_available_captions(video_url)
