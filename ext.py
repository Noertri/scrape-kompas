from pathlib import Path
import itertools


data_path = Path("data")

if not data_path.exists():
    data_path.mkdir(parents=True)

counter = itertools.count(start=1)
