from src.Guess import *
from os import system, name as osname
import re


INPUT_NBR = "`--[?]--:"
valid_regex = re.compile(r'(y(es)?)|(o(ui)?)$', flags=re.IGNORECASE)


def screen_clear():
    cmd = "cls" if osname == "nt" else "clear"
    system(cmd)


def display_header_guessing(guess_status, clear_before=True):
    if clear_before:
        screen_clear()
    print(guess_status.str_top_banner())


class Dialoger:

    def __init__(self):
        pass

    def dict_possible_guessers(self, guessers_list):
        guessers = {}
        for i, user in enumerate(guessers_list):
            guessers[i] = user
        return guessers

    def dict_possible_types(self, types_list):
        types = {}
        for i, t in enumerate(types_list):
            types[i] = t
        return types

    def wait_for_guessing(self, guess_status):
        display_header_guessing(guess_status)
        possible_guessers = self.dict_possible_guessers(guess_status.get_guessers())
        str_possible_guessers = '   '.join([f"[{i}] {g.get_name()}" for i, g in possible_guessers.items()])
        entered = input("Waiting for someone trying to guess (enter 'x' to pass) ...")
        guess_status.get_song().pause()
        if entered == 'x':
            return None, None
        if len(possible_guessers) > 1:
            guesser_id = int(input(f"Who tried to guess ?\n{str_possible_guessers}\n{INPUT_NBR}"))
        else:
            guesser_id = 0
        guesser = possible_guessers[guesser_id]
        possible_guess_types = self.dict_possible_types(guess_status.get_guess_types())
        str_possible_guess_types = '   '.join([f"[{i}] {STR_TYPE.get(t)}" for i, t in possible_guess_types.items()])
        type_id = int(input(f"{guesser.get_name()}, what do you want to guess ?\n{str_possible_guess_types}\n{INPUT_NBR}"))
        return guesser, possible_guess_types[type_id]

    def guess_artist(self, guess_status, guesser):
        display_header_guessing(guess_status)
        name = guesser.get_name()
        input(f"{name}, tell us what the name of the artist is !")
        validation = input(f"The artist was {guess_status.song.get_artist()} !! Do we validate {name}'s proposition ?")
        return valid_regex.match(validation)

    def guess_title(self, guess_status, guesser):
        display_header_guessing(guess_status)
        name = guesser.get_name()
        input(f"{name}, tell us what the title of the song is !")
        validation = input(f"The song title was {guess_status.song.get_title()} !! Do we validate {name}'s proposition ?")
        return valid_regex.match(validation)

    def guess_both(self, guess_status, guesser):
        display_header_guessing(guess_status)
        name = guesser.get_name()
        input(f"{name} apparently got the complete pack, tell us the song artist !")
        validation = input(f"The song was {guess_status.song.get_song_info()} !! Do we validate {name}'s proposition ?")
        return valid_regex.match(validation)

    def guess_owner(self, guess_status, guesser, owner):
        display_header_guessing(guess_status)
        name = guesser.get_name()
        possible_owners = self.dict_possible_guessers(guess_status.get_possible_owners(guesser))
        str_possible_owners = '   '.join([f"[{i}] {o.get_name()}" for i, o in possible_owners.items()])
        owner_id = int(input(f"{name}, do you know who added this song to play today ?\n{str_possible_owners}\n{INPUT_NBR}"))
        return owner.get_name() == possible_owners[owner_id].get_name()

    def game_won(self, winner, all_users):
        print(f"We have a winner, congrats {winner.get_name} !!!")
        all_users.sort()
        for user in all_users:
            print(f"{user}")
