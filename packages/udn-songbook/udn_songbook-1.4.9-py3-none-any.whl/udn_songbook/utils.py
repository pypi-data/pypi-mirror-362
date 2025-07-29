"""Utility functions that aren't really class-specific."""
# vim: set ft=python:

import logging
import os
import re
from pathlib import Path
from string import punctuation

import jinja2

from .filters import custom_filters


def make_dir(destdir: str, logger: logging.Logger | None):
    """Attempt to create a directory if it doesn't already exist.

    Raise an error if the creation fails
    """
    if os.path.exists(destdir):
        return True
    else:
        try:
            os.makedirs(destdir)
            return True
        except OSError as E:
            if logger:
                logger.exception(
                    f"Unable to create output dir {E.filename} - {E.strerror}"
                )
            raise


def unpunctuate(name: str, replacement: str = "") -> str:
    """Remove punctuation from the given name.

    Simply removes punctuation from the given name, for ease of sorting.

    Args:
        name(str): the name you want to unpunctuate
        replacement(str): what to replace punctuation with.
    """
    TRANS = {ord(char): replacement for char in punctuation}
    return name.translate(TRANS)


def safe_filename(filename: str) -> str:
    """Remove UNIX-unfriendly characters from filenames.

    Just simple string translation to remove UNIX-unfriendly characters from filenames
    removes the following characters from filenames:

    """
    tt = {ord(char): "_" for char in punctuation if char not in ["#", "-", "_", "."]}
    # this replaces '#' though, so escape that.
    tt.update({ord("#"): "_sharp_"})

    return re.sub(r"_+", r"_", filename.translate(tt))


def renderer(templatedir: Path | None = None) -> jinja2.Environment:
    """Initialise a jinja2 Environment for rendering songsheets.

    This will load templates from a provided path (templatedir),
    or if this is not provided (or doesn't exist), from the
    'templates' directory in this package.

    """
    loaders: list[jinja2.BaseLoader] = [jinja2.PackageLoader("udn_songbook")]

    if templatedir is not None and templatedir.is_dir():
        loaders.insert(0, jinja2.FileSystemLoader(templatedir))

    jinja_env = jinja2.Environment(
        loader=jinja2.ChoiceLoader(loaders),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols"],
    )

    # add our custom filters
    jinja_env.filters.update(custom_filters)

    return jinja_env
