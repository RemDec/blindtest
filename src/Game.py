from src.AmbientSounder import AmbientSounder
from src.Library import Library
from src.Dialoger import Dialoger
from src.Guess import Guess, ARTIST, TITLE, BOTH_A_T, OWNER
from pathlib import Path
import pygame


class Game:

    def __init__(self, config):
        assets_path = Path(config.get('assets_dir'))
        if not assets_path.is_dir():
            raise ValueError(f"Given directory for assets {assets_path} does not exist")
        self.ambient_sounder = AmbientSounder(assets_path / 'gamesounds')
        self.source_dir = Path(assets_path, 'playlists')
        self.target_score = config.get('target_score', 10)
        self.points_lost_no_guess = config.get('points_lost_noguess', 2)
        self.points_guess = config.get('points_guess', 4)
        self.points_partial_guess = config.get('points_partial_guess', 1)
        self.points_owner_guess = config.get('points_owner_guess', 1)
        self.library = None
        self.users = None
        self.dialog = None
        self.users_kept_blocked = []

    def initialize(self):
        pygame.mixer.init()
        self.library = Library(self.source_dir)
        self.users = self.library.get_users()
        self.dialog = Dialoger()
        print(self.library)

    def start(self):
        while self.check_won() is None:
            self.library.play_current()
            owner_current_song = self.library.get_owner_current_song()
            guess_status = Guess(self.library.get_current_song(), self.users, owner_current_song)
            self.users_kept_blocked = []
            # Displaying music playing, wait for guess interruption
            while self.continue_guessing(guess_status, owner_current_song):
                guesser, guess_type = self.dialog.wait_for_guessing(guess_status)
                if guesser is None:  # Nobody was able to guess
                    self.action_nobody_guessed(owner_current_song, guess_status)
                    continue
                elif guesser.is_same_user(owner_current_song):  # Owner try to guess his own song
                    self.action_user_guess_own_song(guesser, guess_status)
                    self.library.unpause_current()
                    continue
                else:
                    if guess_type == ARTIST:
                        guess_result = self.dialog.guess_artist(guess_status, guesser)
                        self.action_artist_guess(guess_result, guesser, guess_status)
                    elif guess_type == TITLE:
                        guess_result = self.dialog.guess_title(guess_status, guesser)
                        self.action_title_guess(guess_result, guesser, guess_status)
                    elif guess_type == BOTH_A_T:
                        guess_result = self.dialog.guess_both(guess_status, guesser)
                        self.action_both_guess(guess_result, guesser, guess_status)

                    if guess_status.is_song_guessed():
                        #if not guesser.is_blocked:
                        if not guess_status.is_owner_obvious(guesser):
                            guess_owner_result = self.dialog.guess_owner(guess_status, guesser, owner_current_song)
                            self.action_owner_guess(guess_owner_result, guesser, owner_current_song, guess_status)
                    else:
                        self.library.unpause_current()
            # Play next song if possible
            self.library.reset_blocked_users(self.users_kept_blocked)
            if not self.library.play_next():
                print("Achieved one round of playlists")
                self.library.next_round_game_playlist()
        # Game is won by someone, congrats !!!
        self.dialog.game_won(self.check_won(), self.users)

    def continue_guessing(self, guess_status, owner_current_song):
        return self.users_can_still_guess(owner_current_song) and not guess_status.is_song_guessed()

    def action_nobody_guessed(self, owner_current_song, guess_status):
        self.ambient_sounder.play_failed()
        guess_status.set_both_guessed()
        input(f"{owner_current_song.get_name()} nobody knows your song, you loose {self.points_lost_no_guess} points !")
        owner_current_song.loose_points(self.points_lost_no_guess)

    def action_user_guess_own_song(self, guesser, guess_status):
        self.ambient_sounder.play_failed()
        guess_status.set_owner_guessed()
        guesser.set_blocked()
        self.users_kept_blocked.append(guesser.get_name())
        input(f"{guesser.get_name()} trying to guess your own song is not a good idea, you will be blocked next turn..")

    def action_artist_guess(self, guess_result, guesser, guess_status):
        if guess_result:
            self.ambient_sounder.play_bravo()
            guesser.set_blocked()
            guesser.add_points(self.points_partial_guess)
            guess_status.set_artist_guessed()
            print(f"Guessed artist is correct! {guesser.get_name()} you get +{self.points_partial_guess} points but you're out for this round !")
        else:
            self.ambient_sounder.play_failed()
            print(f"Guessed artist is NOT correct! {guesser.get_name()} you're out for the rest of this round !")
            guesser.set_blocked()

    def action_title_guess(self, guess_result, guesser, guess_status):
        if guess_result:
            self.ambient_sounder.play_bravo()
            guesser.set_blocked()
            guesser.add_points(self.points_partial_guess)
            guess_status.set_title_guessed()
            print(f"Guessed title is correct! {guesser.get_name()} you get +{self.points_partial_guess} points but you're out for this round !")
        else:
            self.ambient_sounder.play_failed()
            print(f"Guessed title is NOT correct! {guesser.get_name()} you're out for the rest of this round !")
            guesser.set_blocked()

    def action_both_guess(self, guess_result, guesser, guess_status):
        guess_status.set_both_guessed()
        if guess_result:
            self.ambient_sounder.play_bravo()
            guesser.add_points(self.points_guess)
            print(f"Guessed song is correct! {guesser.get_name()} you get +{self.points_guess} points")
        else:
            self.ambient_sounder.play_failed()
            guesser.set_blocked()
            self.users_kept_blocked.append(guesser.get_name())
            print(f"You guessed it wrong {guesser.get_name()} and revealed the song ... you will be out for next round")

    def action_owner_guess(self, guess_result, guesser, owner, guess_status):
        if guess_result:
            self.ambient_sounder.play_bravo()
            guesser.add_points(self.points_owner_guess)
            guess_status.set_owner_guessed()
            print(f"{guesser.get_name()} you were right, {owner.get_name()} added the song ! You get +{self.points_owner_guess} points.")
        else:
            self.ambient_sounder.play_failed()
            print(f"{guesser.get_name()} you are wrong, that's {owner.get_name()} that added the song !")

    def check_won(self):
        for user in self.users:
            if user.is_winner(self.target_score):
                return user

    def users_can_still_guess(self, owner_current_song):
        #print("USERS EN LICE ", [u.get_name() for u in self.users if u.can_guess() and not u.is_same_user(owner_current_song)])
        return [u for u in self.users if u.can_guess() and not u.is_same_user(owner_current_song)]
