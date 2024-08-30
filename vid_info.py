from pytube import YouTube

# Például egy YouTube videó URL-je
video_url = "https://www.youtube.com/watch?v=0Co1Iptd4p4"

# YouTube objektum létrehozása
yt = YouTube(video_url)


# print(f"Cím: {yt.title}")
# print(f"Szerző: {yt.author}")
# print(f"Publikálás dátuma: {yt.publish_date}")
# print(f"Videó megtekintések száma: {yt.views}")
# print(f"Videó hossza (másodpercben): {yt.length}")
# print(f"Videó leírása: {yt.description}")

print(f"Videó leírása: {yt.fmt_streams}")

streams = yt.streams.filter(file_extension='mp4')
#
print("Elérhető felbontások:")
for stream in streams:
    print(f"{stream.resolution} - {stream.mime_type} - {stream.filesize // (1024 * 1024)} MB")
