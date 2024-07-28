from pprint import pprint
import zlib

from utils_utils import find_repo_gyat


def gyat_log(cur_repo: str, commit_sha: str) -> None:

    parent_dir = find_repo_gyat(cur_repo)

    def recursia(cur_com_sha: str, num: int = 0):

        try:
            with open(
                 parent_dir / "objects" /
                 (cur_com_sha[:2] + "/" + cur_com_sha[2:]), mode="rb"
                 ) as commit:

                data_decompressed = zlib.decompress(commit.read())
                _, content = data_decompressed.split(b"\0", 1)

                parsed_commit = content.decode("utf-8").split("\n")
                pprint(parsed_commit)

                # Yeah hardcoded it, but commit structure probably
                # never going to change so, its ok
                if "parent" in parsed_commit[1]:
                    recursia(parsed_commit[1].strip().split()[1], num-1)
                else:
                    return (f"     {parsed_commit[-1]}\n"
                            f"     ( {num + -num} )\n   "
                            "            |              ")

        except FileNotFoundError:
            print(f"File: {cur_com_sha[:2] + cur_com_sha[2:]} wasnt found")

    recursia(commit_sha)
