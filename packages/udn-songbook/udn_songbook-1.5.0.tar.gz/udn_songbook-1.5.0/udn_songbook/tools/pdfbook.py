#!/usr/bin/env python
"""Render a songbook from a list of content."""
# steps
# 1. Build book via udn-songbook
# 2. Batch index
# 3. Append pages

import argparse
import sys
from datetime import datetime
from itertools import batched
from pathlib import Path

from loguru import logger
from tqdm import tqdm
from weasyprint import CSS, HTML  # type: ignore[import-untyped]
from weasyprint.text.fonts import FontConfiguration  # type: ignore[import-untyped]

from udn_songbook import SongBook
from udn_songbook.utils import renderer

DATEFMT = "%Y-%m-%d.%H%M%S"
NOW = datetime.now()


def parse_cmdline(argv: list[str] = sys.argv[1:]) -> argparse.Namespace:
    """Process commandline arguments."""

    parser = argparse.ArgumentParser(
        description="Publish a PDF songbook from a series of inputs",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "sources",
        nargs="+",
        type=Path,
        help="one or more input sources (directories or files) "
        "for UDN-formatted content",
    )

    parser.add_argument(
        "-p",
        "--profile",
        help="Book profile to generate, these are defined in `defaults.toml` "
        "in the udn-songbook installation dir, or in your songbook source dirs.",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path(f"songbook-{NOW.strftime(DATEFMT)}.pdf"),
        help="output filename for generated book, can be an absolute path. "
        "Any parent directories will be created, if possible",
    )

    parser.add_argument(
        "-t",
        "--title",
        default="Songbook",
        help="title for songbook, will be on index page.",
    )

    parser.add_argument(
        "-b",
        "--batch",
        type=int,
        default=100,
        help="Number of index entries per index page.",
    )

    parser.add_argument(
        "--index-only",
        action="store_true",
        help="Only generate index pages (for testing)",
    )

    parser.add_argument(
        "--templates", type=Path, help="Directory containing custom jinja2 templates."
    )

    args = parser.parse_args(argv)

    logger.info("Ignoring any sources that do not exist.")
    args.sources = [s for s in args.sources if s.exists()]

    return args


def main():
    opts = parse_cmdline(sys.argv[1:])

    print(f"* Collating songbook [profile: {opts.profile}]")

    book = SongBook(
        inputs=opts.sources,
        title=opts.title,
        profile=opts.profile,
        template_paths=opts.templates,
    )

    profile = book.settings.get(f"profile.{opts.profile}", {})

    book.style = Path(book.styles_dir) / Path(
        profile.get("stylesheet", "portrait.css")
    ).with_suffix(".css")

    opts.output.parent.mkdir(exist_ok=True, parents=True)

    jinja_env = renderer()

    # load the index template
    idx_tpl = jinja_env.get_template(book.index_template)

    # let's do the index thing...
    index_batches = list(batched(book.index.items(), opts.batch))

    # template vars
    # book
    # entries
    # A list of PDF docs rendered from templates
    docs = []
    fntc = FontConfiguration()
    css = [CSS(filename=s, font_config=fntc) for s in book.style]
    print("* Generating index")
    for page, entries in enumerate(index_batches):
        raw = idx_tpl.render(
            book=book,
            entries=entries,
            index_id=f"{page:02d}",
            index_count=len(index_batches),
            output="pdf",
            page=page,
            **profile,
        )
        doc = HTML(string=raw).render(
            stylesheets=css,
            presentational_hints=True,
            font_config=fntc,
            optimize_size=("fonts", "images"),
        )

        docs.append(doc)

    if opts.index_only:
        print("* Skipping songsheets (--index-only)")

    else:
        print(f"* Rendering {len(book.contents)} songs")
        for song in tqdm(book.contents, ascii=False, ncols=80):
            logger.info(f"Processing {song.songid}")
            docs.append(
                song.pdf(
                    profile=opts.profile,
                    environment=jinja_env,
                    index_target="#index_00",
                    navigation=True,
                    output="pdf",
                )
            )

    logger.info("Building book")
    all_pages = [p for d in docs for p in d.pages]

    print(f"* Writing PDF to {opts.output}")

    docs[0].copy(all_pages).write_pdf(
        target=opts.output,
        stylesheets=css,
        presentational_hints=True,
        optimize_images=True,
    )


if __name__ == "__main__":
    main()
