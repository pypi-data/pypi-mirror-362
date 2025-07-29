# vim: set ft=python ts=4 sts=2 sw=4 et ci nu:
# wrapper around jinja2 so we can call it
# from both song and book, and potentially
# override or replace it
import logging
import os

# for function annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2
    from dynaconf import settings  # type: ignore[import-untyped]

import udn_songbook

from .filters import custom_filters


class HTMLPublisher:
    """
    Generic class, will call out to jinja2 or any other rendering
    engine we choose to use

    All SOng objects contain HTML markup, these classes are intended to
    use that to output HTML documents
    """

    def __init__(
        self,
        songbook: udn_songbook.book.SongBook,
        destdir: str,
        templatedirs: list[str] = settings.TEMPLATEDIRS,
        stylesheets: list[str] = settings.STYLESHEETS,
    ):
        """
        creates  a jinja2 environment, loading templates from the specified
        directory, falling back on templates defined in this package

        Same applies to css. Should probably move over to sass/scss but there you go.

        Args:
            songbook(udn_songbook.book.SongBook): songbook object to publish
            destdir(str): top-level directory into which you want it published

        KWargs:
            templatedirs(list[str]): list of directories to search for templates
            stylesheets(list[str]): list of stylesheets to include in output
        """
        self.book = songbook
        self.topdir = destdir
        self.stylesheets = stylesheets

        self.env = jinja2.Environment(
            loader=jinja2.ChoiceLoader([
                jinja2.FileSystemLoader(templatedirs),
                jinja2.PackageLoader("udn_songbook", "templates"),
            ])
        )
        # update the filter list
        self.env.filters.update(custom_filters)

    def build_structure(self, layout: list[str] = settings.LAYOUT):
        """
        Creates a directory structure into which we write our files
        """
        if not os.path.exists(self.topdir):
            try:
                os.makedirs(self.topdir)
            except OSError as E:
                self.book.__log(
                    f"Unable to create output dir {E.filename} - {E.strerror}",
                    logging.ERROR,
                )
                raise

        for dname in sorted(layout):
            try:
                os.makedirs(os.path.join(self.topdir, dname))
            except OSError as E:
                self.book.__log(
                    f"Unable to create output dir {E.filename} - {E.strerror}",
                    logging.ERROR,
                )
                raise

    def render(self, songbook: udn_songbook.book.SongBook, **kwargs):
        """
        top-level rendering method, which uses the two following methods
        to render and link the index and
        """

    def render_index(self, context: dict, template: str = "index.html.j2", **kwargs):
        """
        Render the chose templated  with the provided context
        The template will be searched for in the given paths, in order, stopping at
        first match - if no template directories are provided, uses the templates
        from this package.
        """
        tpl = self.env.get_template(template)
        return tpl.render(context, **kwargs)

    def render_song(self, context: dict, template: str = "song.html.j2", **kwargs):
        pass


class PDFPublisher(HTMLPublisher):
    """
    The PDF Renderer processes one or more songsheets
    and returns them as rendered PDF docs.
    """

    pass
