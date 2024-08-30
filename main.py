from pytube import YouTube


def download_youtube_video(url, output_path='.'):
    try:
        # YouTube objektum létrehozása
        yt = YouTube(url)

        # Legjobb minőségű videó stream kiválasztása
        ys = yt.streams.get_highest_resolution()

        # Letöltés indítása
        print(f"Letöltés indítása: {yt.title}")
        ys.download(output_path)
        print(f"Letöltés befejezve: {yt.title}")
    except Exception as e:
        print(f"Hiba történt a letöltés során: {e}")


if __name__ == "__main__":
    video_url = 'https://www.youtube.com/watch?v=0Co1Iptd4p4'
    download_path = './movies'

    download_youtube_video(video_url, download_path)

