import time
from pathlib import Path
from src.Game import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    g = Game({'assets_dir': Path("./assets")})
    g.initialize()
    g.start()
    time.sleep(1000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
