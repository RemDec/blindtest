from src.User import User
from src.Song import SongSource, Song
from src.Playlist import Playlist
from pygame import mixer as mx


class Library:

    def __init__(self, source_dir):
        self.source_dir = source_dir
        self.game_playlist = self.build_game_playlist()
        self.current_song = None

    def build_playlist_from_dir(self, user_dir):
        username = user_dir.name
        user = User(username)
        songs = []
        for format in ['mp3', 'wav', 'flac']:
            songs += [Song(SongSource(format, song_file)) for song_file in user_dir.glob(f"*.{format}")]
        return Playlist(f"{username}'s playlist", user, songs)

    def build_game_playlist(self):
        playlists = []
        for user_dir in self.source_dir.iterdir():
            if user_dir.is_dir():
                playlists += [self.build_playlist_from_dir(user_dir)]
        return Playlist("Game playlist", user=None, playable_content=playlists, random_seq=True)

    def play_current(self):
        self.current_song = self.game_playlist.play()

    def pause_current(self):
        mx.music.pause()

    def unpause_current(self):
        mx.music.unpause()

    def play_next(self):
        if self.game_playlist.jump_next():
            self.play_current()
            return True
        return False

    def fadeout_current_song(self, time_ms=2000):
        print("start fading")
        mx.music.fadeout(time_ms)
        print("finish fading")

    def next_round_game_playlist(self):
        self.game_playlist.reset_sequence()

    def reset_blocked_users(self, ignore_names=None):
        [u.unblock() for u in self.get_users() if (ignore_names is None) or not(u.get_name() in ignore_names)]

    def get_users(self):
        users = []
        for playlist in self.game_playlist.get_contents():
            user = playlist.get_user()
            if (user is not None) and not(user.name in [u.get_name() for u in users]):
                users.append(user)
        users.sort()
        return users

    def get_current_song(self):
        return self.current_song

    def get_owner_current_song(self):
        return self.game_playlist.get_owner_current_content()

    def __str__(self):
        return f"Library generated from {self.source_dir}:\n{self.game_playlist}"
