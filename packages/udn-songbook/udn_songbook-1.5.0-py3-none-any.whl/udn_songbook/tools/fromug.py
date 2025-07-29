#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

import jmespath
import requests
from bs4 import BeautifulSoup as bs
from jmespath import functions

CRD = re.compile(r"(\[ch])(.*?)(\[/ch])")
TAB = re.compile(r"\[/?tab]")


class PathFunctions(functions.Functions):
    @functions.signature(
        {"types": ["string"]},
        {"types": ["string"]},
        {"types": ["string"]},
    )
    def regex_replace(data: str, pattern: str, replacement: str = "") -> str:
        """Allows us to do regex replacement on jmespath objects"""
        p = re.compile(pattern)
        return p.sub(replacement, data)


OPTIONS = jmespath.Options(custom_functions=PathFunctions())


def parse_cmdline(argv: list[str]) -> argparse.Namespace:
    """
    Process commandline options
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url to an ultimate-guitar page")
    parser.add_argument("-o", "--output", help="output file name")
    parser.add_argument(
        "--dump",
        action="store_true",
        default=False,
        help="Dump the source data to a json file for later inspection",
    )

    opts = parser.parse_args(argv)

    if opts.output:
        opts.output = Path(opts.output)

    return opts


def parse_ug(url: str) -> dict:
    """
    process the content of a UG page

    Args:
        url: URL to ultimate Guitar Page

    Returns:
        data: dict
    """
    # data_div = bs(response).find('div', {'class': 'js-store'})
    # metadata = data_div['data-content']
    # data['store']['page']['data']['tab_view']['wiki_tab']['content']
    response = requests.get(url)
    output = {}
    if response.ok:
        # track down the data
        soup = bs(response.content, features="lxml")
        blob = json.loads(soup.find("div", {"class": "js-store"})["data-content"])

        pagedata = blob["store"]["page"]["data"]

        # pd = jmespath.search(
        #     """
        #     {
        #         artist: tab.artist_name,
        #         title: tab.song_name,
        #         raw: regex_replace(tab_view.wiki_tab.content, TAB, ""),
        #         meta: {
        #             artist: tab.artist_name,
        #             title: tab.song_name,
        #             source: tab.tab_url,
        #             original_key: tab.tonality_name,
        #             transcriber: tab.username
        #         }
        #     }
        #     """,
        #     pagedata,
        #     options=OPTIONS,
        # )

        # include artist and title for metadata
        output["artist"] = pagedata["tab"]["artist_name"]
        output["title"] = pagedata["tab"]["song_name"]
        # remove the [/?tab] delimiters, they just get in the way
        output["raw"] = TAB.sub("", pagedata["tab_view"]["wiki_tab"]["content"])
        output["parsed"] = parse_tab(output["raw"].splitlines())

        output["dump"] = pagedata

        # add in a few metadata fields which we can extract from the raw JSON
        output["meta"] = {
            "artist": pagedata["tab"].get("artist_name"),
            "title": pagedata["tab"].get("song_name"),
            "original_key": pagedata["tab"].get("tonality_name"),
            "source": pagedata["tab"].get("tab_url"),
            "transcriber": pagedata["tab"].get("username"),
        }

    return output


def parse_tab(tablines: list[str]) -> list[str]:
    """
    parses the custom format used by UG into a more UDN-like one
    - removes [/?tab] markers
    - strips [ch]CHORD[/ch] wrappers
    - inserts chords into the appropriate positions on lyric lines
    """
    parsed = []
    # while we have unprocessed lines
    while len(tablines):
        # get the next line
        curline = tablines.pop(0)
        if curline.strip() == "":
            # preserve empty lines
            parsed.append(curline)
        elif CRD.search(curline) is not None:
            # this line contains chords
            try:
                # is the next line a non-chord (lyric) line?
                if CRD.search(tablines[0]) is None:
                    lyricline = list(tablines.pop(0))
                    for i, crd in enumerate(CRD.finditer(curline)):
                        # we shift left by multiples of the enclosing tags
                        # i.e. len([ch]) + len([/ch]) x (no. chords already seen - 1)
                        # the -1 reflects the fact that the lyric line gets one entry
                        # longer every time we insert a chord.
                        insert_pos = crd.start() - i * (len(crd[1]) + len(crd[3]) - 1)
                        lyricline.insert(insert_pos, f"({crd[2]})")
                    parsed.append("".join(lyricline))
                else:
                    # next line is chords as well
                    # do a global search and replace:
                    # this also removes leading pipe chars which are
                    # special in ukedown/markdown
                    parsed.append(CRD.sub(r"(\2)", curline).lstrip("|"))
            except IndexError:
                # there is no next line, replace any chords on this one and add it
                parsed.append(CRD.sub(r"(\2)", curline).lstrip("|"))
        else:
            parsed.append(curline)

    return parsed


def main():
    """
    main functionality
    """
    opts = parse_cmdline(sys.argv[1:])
    blob = parse_ug(opts.url)

    if not opts.output:
        opts.output = Path(
            f"{blob['title']} - {blob['artist']}.udn".replace(" ", "_").lower()
        )

    if opts.dump:
        with open(opts.output.with_suffix(".json"), "w") as metafile:
            metafile.write(json.dumps(blob["dump"], indent=2))

    with open(opts.output, "w") as dumpfile:
        dumpfile.write(f"{blob['title']} - {blob['artist']}\n")
        dumpfile.write("\n".join(blob["parsed"]))
        # add in metadata
        if blob["meta"]:
            dumpfile.write("\n\n")
            dumpfile.write("; # metadata\n")
            for k, v in blob["meta"].items():
                if v is not None:
                    dumpfile.write(f"; {k}: {v}\n")


if __name__ == "__main__":
    main()
