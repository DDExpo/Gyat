from pathlib import Path


GYAT_OBJECTS: Path = Path(".gyat/objects")
GYAT_OBJECTS_FILES: set[str] = set(("commit", "tag", "blob"))
GYAT_REFS: Path = Path(".gyat/refs")
GYATIGNORE_DIR: set[str] = set((".gyat", ))
REFS_NAMES: set[str] = set()

INVALID_CHARS_TAG = set(
    ' ', '~', '^', ':', '?', '*', '[', '\\', '..',
    '.lock', '/', '//', '@{', '@'
)

BASE_DIR: Path = Path(__file__).parent

MAIN_ICON: Path = BASE_DIR / Path("graphic/main_ico.png")

# without init as its the command what init gyat dir in the first place
GYAT_COMMANDS: set[str] = set(
    ("commit_tree", "tag", "commit", "cat_file", "add", "hash_object",
     "show_ref", "write_tree", "ls_tree"))

USER_EMAIL: str = "danilvall2001@gmail.com"
USER_NAME: str = "Danil"
