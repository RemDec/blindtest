from tinytag import TinyTag
from pygame import mixer as mx
import io


class SongSource:

    def __init__(self, source_type, source_target):
        self.source_type = source_type
        self.obj_to_read = None
        self.tags = {'artist': "Unknown artist", 'album': "Unknown album", 'title': "Unknown title", 'year': "No date"}

        if source_type in ['mp3', 'wav', 'flac']:
            self.load_from_file(source_target)

    def load_from_file(self, path):
        got_tags = TinyTag.get(path).as_dict()
        for tagname in self.tags:
            if got_tags.get(tagname):
                self.tags[tagname] = got_tags[tagname]
        with open(path, 'rb') as fb:
            self.obj_to_read = fb.read()

    def get_obj_to_read(self):
        return io.BytesIO(self.obj_to_read)

    def __getitem__(self, item):
        return self.tags.get(item)


class Song:

    def __init__(self, song_source, user=None):
        self.song_source = song_source
        self.play_status = False
        self.user =user

    def get_artist(self):
        return self.song_source['artist']

    def get_album(self):
        return self.song_source['album']

    def get_title(self):
        return self.song_source['title']

    def get_year(self):
        return self.song_source['year']

    def play(self):
        self.play_status = True
        #print("Prepare to play", self)
        mx.music.load(self.song_source.get_obj_to_read())
        mx.music.play()
        return self

    def pause(self):
        if self.play_status:
            self.play_status = False
            #print("Pausing", self)
            mx.music.pause()
        return self

    def stop(self):
        self.play_status = False
        #print("Stopping", self)
        mx.music.stop()
        return self

    def jump_next(self):
        self.stop()

    def get_current_status(self):
        return self.play_status

    def get_user(self):
        return self.user

    def get_name(self):
        return self.get_title()

    def get_song_info(self, play_marker=True, mask_artist=False, mask_title=False):
        marker = (" ▶ " if self.play_status else " □ ") if play_marker else ""
        artist = "?" * len(self.get_artist()) if mask_artist else self.get_artist()
        title = "?" * len(self.get_title()) if mask_title else self.get_title()
        year = '????' if mask_title else self.get_year()
        return f"{marker}{artist} - {title} ({year})"

    def __str__(self):
        #status = "▶" if self.play_status else "□"
        #date = f"({self.get_year()})" if self.get_year() else ''
        #return f" {status} {self.get_song_info()} {date}  [{self.get_album()}]"
        return self.get_song_info(mask_artist=False, mask_title=False)