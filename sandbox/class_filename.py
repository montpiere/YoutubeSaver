import re

video_title = "Inside The World’s Most Secret House Built Into a Mountain (House Tour)"


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


file_names = FileName(video_title)

# Fájlnevek megjelenítése
print(f"Fájlnév: {file_names.filename}")
print(f"Videó fájlnév: {file_names.filename_video}")
print(f"Audió fájlnév: {file_names.filename_audio}")
