#!/usr/bin/env python
import argparse
import sys
from pathlib import Path

from udn_songbook import Song


def parse_cmdline(argv: list[str] = sys.argv[1:]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename",
        type=Path,
        nargs="+",
        help="Path to a UDN-format songsheet file",
    )

    return parser.parse_args(argv)


def main():
    opts = parse_cmdline(sys.argv[1:])
    for f in opts.filename:
        song = Song(Path(f))
        print(song)
        print(song.chords)


if __name__ == "__main__":
    main()
