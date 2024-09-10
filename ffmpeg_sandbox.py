import ffmpeg


def merge_video_audio(video_file, audio_file, output_file):
    try:
        # FFmpeg segítségével a videó és audió fájlok egyesítése
        input_video = ffmpeg.input(video_file)
        input_audio = ffmpeg.input(audio_file)

        # Videó és audió kombinálása és mentése
        ffmpeg.output(input_video, input_audio, output_file).run(overwrite_output=True)

        print(f"A fájlok egyesítése sikeres: {output_file}")
    except ffmpeg.Error as e:
        print(f"Hiba történt a fájlok egyesítése során: {e.stderr.decode('utf-8')}")


if __name__ == "__main__":
    video_file = input("Add meg a videó fájl nevét: ")
    audio_file = input("Add meg a hang fájl nevét: ")
    output_file = input("Add meg az egyesített fájl nevét (pl. 'output.mp4'): ")
    COMPLETE_PATH = './complete'
    INCOMPLETE_PATH = './incomplete'


    merge_video_audio(video_file, audio_file, output_file)
