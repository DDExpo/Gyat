import argparse
from pathlib import Path


GYAT_OBJECTS: Path = Path(".gyat/objects")
GYATIGNORE: set[str] = set((".gyat", ))
BASE_DIR: Path = Path(__file__).parent

MAIN_ICON: Path = BASE_DIR / Path('graphic/main_ico.png')

USER_EMAIL: str = "danilvall2001@gmail.com"
USER_NAME: str = "Danil"

PARSER = argparse.ArgumentParser()
argsubparsers = PARSER.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True
