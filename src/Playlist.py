from random import shuffle


class Playlist:

    def __init__(self, name, user=None, playable_content=None, random_seq=False, end_cb=None):
        self.name = name
        self.user = user
        self.random_seq = random_seq
        self.play_sequence = []
        self.seq_pointer = 0
        self.playable_content = playable_content if playable_content else []
        self.generate_play_sequence(self.playable_content)
        self.end_callback = end_cb

    def generate_play_sequence(self, new_content=None):
        if new_content is None:
            new_content = self.playable_content
        self.play_sequence = list(range(len(new_content)))
        if self.random_seq:
            shuffle(self.play_sequence)

    def reset_sequence(self, new_content=None):
        self.pause()
        self.seq_pointer = 0
        self.generate_play_sequence(new_content)

    def get_current_content(self):
        index_from_sequence = self.play_sequence[self.seq_pointer]
        return self.playable_content[index_from_sequence]

    def play(self):
        return self.get_current_content().play()

    def pause(self):
        self.get_current_content().pause()

    def current_content_jump_next(self):
        self.get_current_content().jump_next()

    def jump_next(self, current_content_jump=True):
        self.pause()
        if current_content_jump:
            self.current_content_jump_next()
        if self.seq_pointer >= len(self.play_sequence) - 1:
            #print(self.name, "FINISHED SEQUENCE")
            self.seq_pointer = 0
            return False
        else:
            self.seq_pointer += 1
            return True

    def get_name(self):
        return self.name

    def get_contents(self):
        return self.playable_content

    def get_user(self):
        return self.user

    def get_owner_current_content(self):
        return self.get_current_content().get_user()

    def __str__(self):
        owner = self.user if self.user else "Global"
        content = '\n'.join([f"  | {playable}" for playable in self.playable_content])
        return f"{self.name} by {owner} {self.play_sequence} {self.seq_pointer}\n{content}"