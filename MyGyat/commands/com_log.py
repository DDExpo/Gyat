import zlib
from pprint import pprint
from pathlib import Path

from const import GYAT_OBJECTS


def gyat_log(cur_repo: Path, commit_sha: str) -> None:

    def recursia(cur_com_sha: str, num: int = 0):

        try:
            with open(
                 cur_repo / GYAT_OBJECTS /
                 (cur_com_sha[:2] + "/" + cur_com_sha[2:]), mode="rb"
                 ) as commit:

                data_decompressed = zlib.decompress(commit.read())
                header, content = data_decompressed.split(b"\0", 1)

                parsed_commit = content.decode("utf-8").split("\n")
                pprint(parsed_commit)

                # Yeah hardcoded it, but commit structure probably
                # never going to change so, its ok
                if "parent" in parsed_commit[1]:
                    recursia(parsed_commit[1].strip().split()[1], num-1)
                return (f"     {parsed_commit[-1]}\n"
                        f"     ( {num + -num} )\n   "
                        "            |              ")

        except FileNotFoundError:
            print(f"File: {cur_com_sha[:2] + cur_com_sha[2:]} wasnt found")
            return

    recursia(commit_sha)
