#!/usr/bin/env python3
"""Class-based wrapper representing a song."""
# vim: set ts=4 sts=4 sw=4 et ci nu ft=python:

# object-oriented wrapper around song objects
import datetime
import hashlib
import io
import re
import sys

# path manipulation
from pathlib import Path

# for type hinting
from typing import IO, Any

import jinja2
import markdown

# HTML processing, rendering and manipulation
import yaml
from bs4 import BeautifulSoup as bs
from pychord import Chord, QualityManager  # type: ignore

# PDF rendering
from weasyprint import CSS, HTML  # type: ignore
from weasyprint.text.fonts import FontConfiguration  # type: ignore

from .config import load_settings

# jinja filters and general utils
from .filters import custom_filters
from .utils import renderer

# a slightly doctored version of the ukedown chord pattern, which separates
# '*' (and any other non-standard chord 'qualities' so we can still transpose
CHORD = r"\(([A-G][adgijmnsu0-9#b\/A-G]*)([*\+])?\)"
CRDPATT = re.compile(CHORD)


class Song:
    """
    A Song object represents a song.

    It has associated methods to generate output, summarise content etc
    and is instantiated from a ukedown filename, an open file handle, or a string.

    This wrapper is intended to make it simpler to construct a DB model
    for this content, plus to take all this code out of any automation
    scripts
    """

    def __init__(self, src: IO | str | Path, **kwargs):
        """
        Construct our song object from a ukedown (markdown++) file.

        Args:
            src can be one of the following
            src(str):        ukedown content read from a file.
                             This must be unicode (UTF-8)
            src(file handle): an open file handle (or equivalent object)
                             supporting 'read' (stringIO etc).
                             This should produce UTF-8 when read
                             (codecs.open is your friend)
            src(path):       path to a ukedown-formatted file to open and parse
            kwargs:          key=value pairs, see below

        Kwargs:
            anything can be customised, most attributes/properties are
            auto-generated, but we sometimes need to override them.
            Those listed below are commonly-used properties.
            These can also be parsed out of the songsheet itself
            using metadata markup

            title(str):      Song Title
            title_sort(str): Song title in sortable order
            artist(str):     artist name, as printed
            artist_sort:     sortable artist name, usually either
                             "Surname, Firstname" or "Band Name, The"
                             where appropriate.
            tags(list):      tags to apply to this song (tentative, tested etc)
            template(path):  the jinja2 template used to render this song.
                             can be overridden at the songbook level
            id(int):         page number, used as part of the "id" attribute on
                             headers
        """
        self._checksum: str | None = None
        self._load_time: datetime.datetime = datetime.datetime.now()
        self._mod_time: datetime.datetime | None = None
        self._index_entry: str | None = None
        self._id: int = 0
        self.location: Path = Path(__file__).parent
        self.styles_dir: Path = self.location / "stylesheets"
        self._settings = load_settings()

        if isinstance(src, Path):
            # did we pass a filename?
            # This is the most common use case
            self._filename: Path | None = src
            self.__load(self.filename)
            self._fsize = self.filename.stat().st_size
        elif isinstance(src, str):
            # presume we've been given content
            self._filename = None
            self._markup: str = src
            self._fsize = len(src)  # type: ignore
        elif isinstance(src, IO) and hasattr(src, "read"):
            # if we're operating on a filehandle
            # or another class that implements 'read'
            self._markup = str(src.read())
            self._filename = Path(src.name) if hasattr(src, "name") else None
            self._fsize = len(src.read())
        else:
            raise TypeError(
                "Incompatible data passed to Song. "
                "Must be a Path, str (content), or a file-like object"
            )
        # arbitrary metadata, some of which will have meaning
        self._meta: dict[str, Any] = {}
        # tags are separate
        self._tags: set[str] = set([])

        self.__parse(markup=self._markup)

        # set a default template (loaded from this package) if one was not provided
        # (e.g. from a songbook containing this song)
        self._template = kwargs.get("template", "song.html.j2")

        # update with any parameters...
        for key, val in kwargs.items():
            setattr(self, key, val)

        if self._filename is None:
            self._filename = Path(f"{self.title}_-_{self.artist}.udn".lower())

        if self._index_entry is None:
            self._index_entry = f"{self.title} - {self.artist}"

        self.__checksum()

    def __unicode__(self):
        """Get unicode string representation."""
        return self.songid

    def __str__(self):
        """Get string representation."""
        return self.songid

    def __repr__(self):
        """Show representation."""
        return f"<Song: {self.songid}>"

    # other 'private' methods for use in __init__, mostly.

    def __load(self, sourcefile: Path):
        """Load udn content from a file.

        sets:
            self._markup(str): text content, amy include metadata
            self._mod_time(datetime): last modified time, if any
            self.fsize(int): size of input in bytes.
        """
        try:
            fileprops = sourcefile.stat()
            self._markup = sourcefile.read_text(encoding="utf-8")
            self._mod_time = datetime.datetime.fromtimestamp(fileprops.st_mtime)
            self.fsize = fileprops.st_size

        except OSError as E:
            print(f"Unable to open input file {E.filename} ({E.strerror}")
            self._markup = ""

    def __checksum(self):
        """Generate sha256 checksum of loaded content.

        intended to use for change detection

        sets:
            self._checksum: sha256 hash of content
        """
        shasum = hashlib.sha256()
        shasum.update(self._markup.encode("utf-8"))
        self._checksum = shasum.hexdigest()

    def __extract_meta(self, markup: str | None = None, leader: str = ";"):
        """Parse out metadata from file.

        This MUST be done before passing to markdown
        There doesn't have to be any metadata - should work regardless

        Args:
            markup(str): content of file, which we will manipulate in place
            leader(str): leader character - only process lines that begin with this

        sets:
            self._markup(str): cleaned markdown/udn without metadata
            self._meta(dict): metadata (if any) extracted from markup
        """
        if markup is None:
            markup = self._markup
        metap = re.compile(rf"^{leader}\s?(.*)", re.I | re.U)
        metadata = []
        content = []

        for line in markup.splitlines():
            res = metap.match(line)
            if res is not None:
                metadata.append(res.group(1))
            else:
                content.append(line)
        self._markup = "\n".join(content)
        if len(metadata):
            self._meta = yaml.safe_load("\n".join(metadata)) or {}
        else:
            self._meta = {}

    def __parse(self, **kwargs):
        """Parse ukedown to set attrs and properties.

        Process metadata entries in file, convert markup content to HTML

        kwargs:
            properties to set on parsed object, usually passed in from __init__
            These override self._meta - so you can set them externally, add tags
            etc willy-nilly.

        sets:
            self._markup

        """
        # strip out any metadata entries from input
        self.__extract_meta(self._markup)

        # this will be the definitive list of tags
        # for this song object
        self._tags.update(self._meta.get("tags", []))

        # convert remaining markup to HTML
        self.__parse_markup()

        # if we override the title (for parsing reasons)
        # in metadata, use that one.
        self._title = self._meta.get("title", self._title)
        self._title_sort = self._meta.get("title_sort", self.title).title()

        self._artist = self._meta.get("artist", self.artist)
        self._artist_sort = self._meta.get("artist_sort", self.artist)

        # extract chords and positions in text/markup
        self.__parse_chords()

    def __parse_markup(self):
        """Convert markup to HTML, set attributes.

        sets:
            self.title:   title (parsed from first line)
            self.artist:  Artist (parsed from first line)
            self.content: HTML content.
        """
        # convert UDN to HTML via markdown + extensions.
        raw_html = markdown.markdown(
            self._markup, extensions=["markdown.extensions.nl2br", "ukedown.udn"]
        )

        # process HTML with BeautifulSoup to parse out headers etx
        soup = bs(raw_html, features="lxml")

        # extract our sole H1 tag, which should be the title - artist string
        hdr = soup.h1.extract()
        try:
            title, artist = (i.strip() for i in hdr.text.split("-", 1))
        except ValueError:
            title = hdr.text.strip()
            artist = None

        # remove the header from our document
        hdr.decompose()

        # set core attributes
        self._title = title
        self._artist = artist

        # add processed body text (with headers etc converted)
        self.body = "".join([str(x) for x in soup.body.contents]).strip()

    def __parse_chords(self):
        """Extract the chords from markup, not HTML.

        This determines their position in the song and allows
        us to write code to transpose them.

        sets:
            self._chord_locations: nested list of chord, start position, end position
            self._chords: deduplicated chords list, in order of appearence.
        """

        # allow us to add new chord "qualities" (voicings, really, like 6sus2 or add#11)
        custom_qualities = self._settings.get("chordtypes", {})
        quality_manager = QualityManager()
        for q, notes in custom_qualities.items():
            quality_manager.set_quality(str(q), notes)

        # contains chord objects, plus their start and end positions in the text
        chord_locations = []
        # an ordered, deduped list of chords (to manage which diagrams we need)
        chordlist = []

        # unparsed chords
        unparsed = []

        # walk over matched chords, convert them and record their locations
        for m in CRDPATT.finditer(self.markup):
            try:
                crd = Chord(m.groups()[0])
            except ValueError:
                # we couldn't parse the chord.
                unparsed.append(m.groups()[0])

            tail = m.groups()[1]
            chord_locations.append([crd, m.end(), tail if tail is not None else ""])
            if crd not in chordlist:
                chordlist.append(crd)

        # set attributes so we can access these elsewhere
        self._chord_locations = chord_locations
        self._chords = chordlist
        self._unknown_chords = unparsed
        if len(unparsed):
            print(f"could not parse these chord names: {', '.join(unparsed)}")

    def __get_render_env(self, templatedir: str = "") -> jinja2.Environment:
        """Initialise a jinja2 Environment for rendering songsheets.

        This will load templates from a provided path (templatedir),
        or if this is not provided (or doesn't exist), from the
        'templates' directory in this package.

        """
        jinja_env = jinja2.Environment(
            loader=jinja2.ChoiceLoader([
                jinja2.FileSystemLoader(templatedir),
                jinja2.PackageLoader("udn_songbook"),
            ]),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
            extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols"],
        )

        # add our custom filters
        jinja_env.filters.update(custom_filters)

        return jinja_env

    def html(
        self,
        environment: jinja2.Environment | None = None,
        template: str = "song.html.j2",
        stylesheet: Path = Path("portrait.css"),
        profile: str | None = None,
        verbose: bool = False,
        output="html",
        **context,
    ) -> str:
        """Render HTML output using jinja templates.

        This defaults to using the templates packaged with `udn_songbook` but you
        can override this with the `templatedir` and `template` parameters

        KWargs:
            templatedir(str): override location for template files
            template(str): name of song template to look for
            context(dict): key=val pairs to add to template context

        Context vars that can be used (template-dependent):
            css_path(str): where are our stylesheets?
            stylesheet(str): which stylesheet should we use (filename)?
        """
        if profile is not None:
            ctx = self._settings.get(f"profile.{profile}", {})
            context.update(ctx)

        if stylesheet is None:
            stylesheet = Path(context.get("stylesheet", "portrait.css")).with_suffix(
                ".css"
            )
        else:
            stylesheet = Path(stylesheet).with_suffix(".css")

        if stylesheet.exists():
            context["stylesheet"] = stylesheet.name
            context["css_dir"] = str(stylesheet.parent)
        elif (self.styles_dir / stylesheet).exists():
            context["stylesheet"] = stylesheet.name
            context["css_dir"] = self.styles_dir
        else:
            print(self.styles_dir)
            print(f"Cannot find stylesheet {stylesheet}")
            sys.exit(2)

        if verbose:
            print("Rendering Context:")
            print(context)

        # use the passed template, if not fall back to the default
        if template is None:
            template = self.template
        # There are prettier ways to do this but this is simple and readable
        # if we provide a jinja environment (e.g. from a parent songbook), use it
        if environment is None:
            environment = renderer()

        tpl = environment.get_template(template)
        return tpl.render(songbook={}, song=self, output=output, **context)

    def pdf(
        self,
        stylesheet: Path = Path("portrait.css"),
        destfile: str | None = None,
        profile: str | None = None,
        **context,
    ):
        """Generate a PDF songsheet from this song.

        Stylesheets are loaded from the udn_songbook installation dir
        by default, but you can provide a path to a stylesheet of your
        choice

        KWargs:
            stylesheet(str): name of, or path to stylesheet
            destfile(str): output file, if needed
            context: dict of options to the template

        Context here is essentially variables supported by the built-in templates.
        If you use your own templates, adjust accordingly
        For the built-in template this means at least the following, which
        control inline CSS in the rendered HTML. All currently default to False.

        chords(bool)    - show inline chord names
        diagrams(bool)  - show chord diagrams(WIP)
        overflow(bool)  - show chord diagram overflow (WIP)
        notes(bool)     - show performance notes

        NB at this time, chord diagrams are not generated - this will use the
        external python-fretboard diagram library
        """
        # load any specified profile and update the context
        if profile is not None:
            ctx = self._settings.get(f"profile.{profile}", {})
            context.update(ctx)

        if stylesheet is None:
            stylesheet = Path(context.get("stylesheet", "portrait.css"))
        else:
            stylesheet = Path(stylesheet)
        # try the stylesheet provided, as follows:
        # load it as an absolute path
        # load it from the included stylesheets
        # fall back to the default "portrait.css"

        fontcfg = FontConfiguration()
        # figure out the stylesheet location
        if stylesheet.exists():
            styles = CSS(filename=stylesheet, font_config=fontcfg)
        elif (self.styles_dir / stylesheet).exists():
            styles = CSS(filename=self.styles_dir / stylesheet, font_config=fontcfg)
        else:
            print(f"Cannot find stylesheet {stylesheet}")
            sys.exit(2)

        content = HTML(string=self.html(**context))
        pdfdoc = content.render(
            stylesheets=[styles],
            presentational_hints=True,
            font_config=fontcfg,
            optimize_size=("fonts", "images"),
        )

        if destfile is not None:
            pdfdoc.write_pdf(target=Path(destfile))
        else:
            return pdfdoc

    def transpose(self, semitones: int):
        """Transpose all chords in the song by the given number of semitones.

        This will alter the following attributes:

        self._markup
        self._chords
        self._chord_locations

        Args:
            semitones(int): number of semitones to transpose by
                negative to tranpose down
        """
        # cannot transpose if we have unknown chords
        if len(self._unknown_chords):
            return
        # take a copy to transpose, as the transposition is an in-place
        # alteration of chord objects
        tmkup = io.StringIO(self._markup)
        transposed = []
        for crd, end, tail in self._chord_locations:
            # change the chord in place
            crd.transpose(semitones)
            # read the section of the markup that contains it
            # and insert the new transposed version
            transposed.append(
                CRDPATT.sub(f"({crd.chord}{tail})", tmkup.read(end - tmkup.tell()))
            )
        # now append the rest of the markup, otherwise we lose anything after the last
        # chord
        transposed.append(tmkup.read())

        # alter the markup in place
        self._markup = "".join(transposed)

        # convert back to HTML
        self.__parse_markup()

        # keep a record of our transposition
        self._meta["transposed"] = semitones

    def save(self, path: Path | None = None):
        """Save an edited song back to disk.

        If path is None, will use the
        original filename (self.sourcefile)

        Args:
            path(str): path to output file, if not in-place
        """
        # did we provide an output file?
        if path is not None:
            outfile = path
        # if not, use the current filename, if it exists
        elif self._filename is not None:
            outfile = Path(self._filename)
        else:
            # create a new filename usingtitle and artist
            outfile = Path(f"{self.title} - {self.artist}.udn")

        self._meta["tags"] = list(self._tags)

        try:
            with outfile.open("w") as output:
                output.write(self.udn())
                # stick the metadata at the bottom
                self._filename = outfile
                print(f"saved song to {outfile}")
        except OSError as E:
            # switch to logging at some point
            print(f"unable to save {E.filename} - {E.strerror}")

    def udn(self) -> str:
        """Returns the UDN markup as a string.

        Used by `self.save` but also handy when called via an API.
        """
        self._meta["tags"] = list(self._tags)
        assembled = [self._markup]
        if self._meta is not None:
            assembled.append("; # metadata")

            assembled.extend([
                f"; {line}"
                for line in yaml.safe_dump(
                    self._meta, default_flow_style=False
                ).splitlines()
            ])

        return "\n".join(assembled)

    # Property-based attribute settings - some are read-only in this interface

    @property
    def markup(self):
        """Fetch current markup content."""
        return self._markup

    @markup.setter
    def markup(self, content):
        """Replace existing markup."""
        self._markup = content

    @property
    def filename(self):
        """Get the song filename."""
        return self._filename

    @filename.setter
    def filename(self, path):
        """Set the song filename."""
        self._filename = Path(path)

    @property
    def artist(self):
        """Get the song artist."""
        return self._artist

    @artist.setter
    def artist(self, value):
        """Set the song artist."""
        self._artist = value

    @property
    def title(self):
        """Get the song title."""
        return self._title

    @title.setter
    def title(self, value):
        """Set the song title."""
        self._title = value

    # no setter for chords, they're parsed from input
    @property
    def chords(self):
        """Get the chords used in the song."""
        return self._chords

    # tags are read-only too (ish)
    @property
    def tags(self):
        """Get song tags."""
        return self._tags

    @tags.setter
    def tags(self, taglist):
        """Replace all song tags."""
        self._tags = set(taglist)

    def tag(self, tag):
        """Set individual song tags."""
        if tag not in self.tags:
            self._tags.add(tag)

    def untag(self, tag):
        """Remove a specific tag."""
        if tag in self._tags:
            self._tags.pop(tag)

    def clear_tags(self):
        """Clear all tags."""
        # remoes ALL tags
        self._tags = set([])

    @property
    def checksum(self):
        """Get the content checksum."""
        return self._checksum

    @property
    def id(self):
        """Get song id."""
        return self._id

    @id.setter
    def id(self, val: int):
        """Set the song id."""
        self._id = val

    @property
    def meta(self):
        """Get song metadata."""
        return self._meta

    @meta.setter
    def meta(self, data, **kwargs):
        """Set or update metadata.

        Can set individual keys or update it all

        kwargs overrides everything else :)
        """
        # actually updates, not replaces
        try:
            self._meta.update(data)
            if len(kwargs):
                self._meta.update(kwargs)
        except TypeError as E:
            raise TypeError("data must be a dict") from E

    @property
    def size(self):
        """Get markup size."""
        return self._fsize

    @property
    def loaded(self):
        """Return the load time."""
        return f"{self._load_time:%Y-%m-%d %H:%M:%S}"

    @property
    def modified(self):
        """Return modification time."""
        return f"{self._mod_time:%Y-%m-%d %H:%M:%S}"

    @property
    def stat(self):
        """Get size, load and modification times."""
        return f"size: {self.fsize}, loaded: {self.loaded}, modified {self.modified}"

    @property
    def artist_sort(self):
        """Get the sortable version of the song artist."""
        return self._artist_sort

    @property
    def title_sort(self):
        """Get the sortable version of the song title."""
        return self._title_sort

    @property
    def songid(self):
        """Get string representation in a songbook index."""
        return self._index_entry

    @songid.setter
    def songid(self, data):
        """Set the string representation of the song."""
        try:
            self._index_entry = str(data)
        except TypeError as E:
            raise TypeError(
                "Song IDs must be strings, or be convertible to strings"
            ) from E

    @property
    def template(self):
        """Name of the template to render this song."""
        return self._template

    @template.setter
    def template(self, value):
        """Change the template used to render the song."""
        self._template = value
