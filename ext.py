from pathlib import Path


data_path = Path("data")

if not data_path.exists():
    data_path.mkdir(parents=True)
    