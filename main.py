from pytube import YouTube, Playlist
from moviepy.editor import VideoFileClip, AudioFileClip
import re
from pathlib import Path
import shutil
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
import datetime


# TOOLS
class FileName:
    def __init__(self, _video_title, _video_id):
        self.filename = f"{self.create_filename(_video_title)}_{_video_id}"
        self.filename_video = f"{self.filename}_video.mp4"
        self.filename_audio = f"{self.filename}_audio.mp4"
        self.filename_caption = f"{self.filename}.srt"

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


def get_videos_from_playlist(playlist_url):
    try:
        playlist = Playlist(playlist_url)
        return playlist.video_urls
    except Exception as e:
        print(f"Hiba történt a lejátszási lista videóinak lekérése során: {str(e)}")
        return []


def extract_video_id(_url):
    # id from URL
    pattern = r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)|youtu\.be/([a-zA-Z0-9_-]+)'
    match = re.match(pattern, _url)

    if match:
        return match.group(1) if match.group(1) else match.group(2)
    else:
        raise ValueError("Bad URL")


def convert_time(seconds):
    td = datetime.timedelta(seconds=seconds)
    time_str = str(td)

    if '.' in time_str:
        hours, minutes, seconds = time_str.split(':')
        seconds, milliseconds = seconds.split('.')
        milliseconds = milliseconds[:3]  # Csak három számjegy az ezredmásodperchez
    else:
        hours, minutes, seconds = time_str.split(':')
        milliseconds = "000"  # Ha nincs ezredmásodperc, 000-t használunk

    return f"{hours.zfill(2)}:{minutes.zfill(2)},{milliseconds}"


# DOWNLOADS
def download_video(_yt):
    available_resolutions = []
    try:
        streams = _yt.streams.filter(only_video=True)
        for video_stream in streams:
            available_resolutions.append(video_stream.resolution)

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
            return

        video_stream = _yt.streams.filter(res=resolution, file_extension="mp4").first()

        if video_stream:
            print(f"Video downloading...")
            video_stream.download(INCOMPLETE_PATH, filename=f"{filenames.filename_video}")
            print(f"Video done")

        return 'done'

    except Exception as e:
        print(f"ERROR with video download: {str(e)}")


def download_audio(_yt):
    try:
        audio_stream = _yt.streams.filter(only_audio=True).first()

        if audio_stream:
            print(f"Audio downloading...")
            audio_stream.download(INCOMPLETE_PATH, filename=f"{filenames.filename_audio}")
            print(f"Audio done")

        else:
            print("No available audio")

    except Exception as e:
        print(f"ERROR with audio download: {str(e)}")


def download_caption(video_url_or_id):
    filename = filenames.filename_caption

    try:
        if "youtube.com" in video_url_or_id or "youtu.be" in video_url_or_id:
            _video_id = extract_video_id(video_url_or_id)
        else:
            _video_id = video_url_or_id
    except ValueError as e:
        print(f"ERROR: {e}")
        return

    try:
        # en
        try:
            transcript = YouTubeTranscriptApi.get_transcript(_video_id, languages=['en'])
        except NoTranscriptFound:
            print("There is no 'en' caption")
            # en-US
            transcript = YouTubeTranscriptApi.get_transcript(_video_id, languages=['en-US'])

    except NoTranscriptFound:
        print("There is no 'en-US' caption")

        # Try in translated captions
        try:
            transcripts = YouTubeTranscriptApi.list_transcripts(_video_id)

            translation = transcripts.find_transcript(transcripts.translation_languages)
            transcript = translation.fetch()
        except NoTranscriptFound:
            print("No available caption there.")
            return
        except TranscriptsDisabled:
            print("The captions are disabled for this video")
            return

    # SRT format
    with open(f"{COMPLETE_PATH}/{filename}", "w", encoding="utf-8") as file:
        for i, entry in enumerate(transcript, 1):
            start_time = convert_time(entry['start'])
            duration = entry.get('duration', 2.0)
            end_time = convert_time(entry['start'] + duration)

            file.write(f"{i}\n")
            file.write(f"{start_time} --> {end_time}\n")
            file.write(f"{entry['text']}\n\n")

    print(f"Caption save to SRT: {filename}")


# MERGE
def merge_video_audio():
    try:
        # Loading video
        video_clip = VideoFileClip(f'{INCOMPLETE_PATH}/{filenames.filename_video}')

        # Loading audio
        audio_clip = AudioFileClip(f'{INCOMPLETE_PATH}/{filenames.filename_audio}')

        # Add audio to video
        video_with_audio = video_clip.set_audio(audio_clip)

        # Save merged file
        video_with_audio.write_videofile(f'{COMPLETE_PATH}/{filenames.filename}.mp4',
                                         codec="libx264",
                                         audio_codec="aac"
                                         )

        print(f"File merging success : {filenames.filename}.mp4")

    except Exception as e:
        print(f"ERROR with merging: {str(e)}")


if __name__ == "__main__":
    dir_path_incomplete = Path("incomplete")
    dir_path_incomplete.mkdir(exist_ok=True)
    dir_path_complete = Path("complete")
    dir_path_complete.mkdir(exist_ok=True)
    print(f"Directory created: {dir_path_incomplete}")

    COMPLETE_PATH = './complete'
    INCOMPLETE_PATH = './incomplete'

    urls = read_urls_from_file()
    print(f'Found {len(urls)} link(s) in file')

    all_video_urls = []
    for url in urls:
        if 'youtube.com/playlist' in url:
            # Playlists
            print(f"Playlist link detected")
            playlist_video_urls = get_videos_from_playlist(url)
            all_video_urls.extend(playlist_video_urls)
        elif 'youtube.com/watch' in url or 'youtu.be' in url:
            # Individual
            all_video_urls.append(url)
        else:
            print(f"Invalid URL format detected: {url}. Skipping...")
            continue

        # Iterate through all video URLs and process them
        for video_url in all_video_urls:
            try:
                # CREATE YT OBJECT
                yt = YouTube(video_url)
                video_title = yt.title
                video_id = yt.video_id
                print(f"\n{video_title}\n{'-' * len(video_title)}")

                # FORMAT FILENAME
                filenames = FileName(video_title, video_id)

                # DOWNLOAD
                video_download_status = download_video(yt)
                if video_download_status != 'done':
                    print("No downloaded video")
                else:
                    download_audio(yt)
                    # Try downloading caption, but do not stop if it fails
                    try:
                        download_caption(video_url)
                    except Exception as er:
                        print(f"Error occurred during caption download: {str(er)}")

                    # Always try to merge video and audio, even if there was an issue with captions
                    merge_video_audio()

            except Exception as er:
                print(f"Error occurred with video: {str(er)}")
                continue

    # REMOVE TEMPORARY DIR
    shutil.rmtree(dir_path_incomplete)
    print(f"Remove temporary dir: {dir_path_incomplete}")
