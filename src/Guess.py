ARTIST = 0
TITLE = 1
BOTH_A_T = 2
OWNER = 3

STR_TYPE = {ARTIST: "Artist name", TITLE: "Song title", BOTH_A_T: "Artist & title", OWNER: "Author"}


class Guess:

    def __init__(self, song, users, owner):
        self.song = song
        self.users = users
        self.owner = owner
        self.status = {ARTIST: False, TITLE: False, BOTH_A_T: False, OWNER: False}

    def str_top_banner(self):
        str_top = " "
        for u in self.users:
            str_top += f"[{u.get_points() if u.can_guess() else 'x'}] {u.get_name()}   "
        info_song = self.song.get_song_info(mask_artist=not(self.status[ARTIST]), mask_title=not(self.status[TITLE]))
        return f"{str_top}\n{info_song}"

    def get_guessers(self):
        return [u for u in self.users if u.can_guess()]

    def get_possible_owners(self, guesser):
        return [u for u in self.users if u.get_name() != guesser.get_name()]

    def is_owner_obvious(self, guesser):
        possible_owners = self.get_possible_owners(guesser)
        if len(possible_owners) <= 1:
            return True
        return False

    def is_song_guessed(self):
        return self.status[BOTH_A_T] or (self.status[ARTIST] and self.status[TITLE])

    def set_artist_guessed(self):
        self.status[ARTIST] = True

    def set_title_guessed(self):
        self.status[TITLE] = True

    def set_both_guessed(self):
        self.status[BOTH_A_T] = True

    def set_owner_guessed(self):
        self.status[OWNER] = True

    def get_song(self):
        return self.song

    def get_guess_types(self, exclude_owner=True):
        return [t for t, guessed in self.status.items() if (not guessed) and not (exclude_owner and t == OWNER)]
