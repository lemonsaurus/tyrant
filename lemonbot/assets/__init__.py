import itertools
import random
from pathlib import Path

# Locate and shuffle files
_assets = Path(__file__).parent
_shuffled = [f for f in _assets.iterdir() if not f.suffix == ".py"]
random.shuffle(_shuffled)

# Public variables
FILE_CYCLE = itertools.cycle(_shuffled)
