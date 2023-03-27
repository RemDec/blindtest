from pathlib import Path
from preferredsoundplayer import soundplay
import random


class AmbientSounder:

    def __init__(self, gamesounds_dir):
        gamesounds_path = Path(gamesounds_dir)
        if not gamesounds_path.is_dir():
            raise ValueError(f"Given directory for gamesounds {gamesounds_path} does not exist")
        self.bravo_dir = gamesounds_path / 'bravo'
        self.bravo_default = self.bravo_dir / 'default' / 'bravo.mp3'
        self.bravo_sounds = list(self.bravo_dir.glob('*.mp3'))
        self.failed_dir = gamesounds_path / 'failed'
        self.failed_default = self.failed_dir / 'default' / 'failed.mp3'
        self.failed_sounds = list(self.failed_dir.glob('*.mp3'))

    def play_bravo(self):
        target = self.bravo_default
        if len(self.bravo_sounds):
            target = random.choice(self.bravo_sounds)
        soundplay(str(target))

    def play_failed(self):
        target = self.failed_default
        if len(self.failed_sounds):
            target = random.choice(self.failed_sounds)
        soundplay(str(target))
