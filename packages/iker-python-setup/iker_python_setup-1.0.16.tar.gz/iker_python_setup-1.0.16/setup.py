import os
import sys

sys.path.append(os.path.join(os.getcwd(), "src"))

from iker.setup import setup

if __name__ == "__main__":
    setup()
