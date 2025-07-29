<!-- markdownlint-disable MD013 MD033-->
<!-- vim: set tw=100 -->

# udn-songbook

## What'cha talkin' about, Willis?

`udn-songbook` is a class-based abstraction of a songbook, using the [ukedown](https://pypi.org/project/ukedown/) rendering engine.
Long-term it is intended to replace most of the code from the [`ukebook-md`](https://github.com/ukebook-md) tools.
In the end, you should be able to take the code from here and create (and render) songbooks with it, producing PDFs and/or HTML
(and possibly other formats, if I add them).

## Requirements

Python packages
* ukedown (markdown extensions)
* weasyprint (PDF generation)
* pychord (chord management)

## development requirements - for future project enhancements
* python-fretboard (chord generation)

## The TL;DR

How to use the current functionality

(it only does basic things at the moment)

```python
from udn_songbook import Song
s = song('/path/to/filename')

# list the unique chords in the song
s.chords

# save it to disk
s.save(outputfile)

# transpose by an arbitrary number of semitones
s.transpose(semitones)

# generate a PDF from the current song, using built-in templates
s.pdf()
```

And to build a songbook, use the SongBook class, with a directory of UDN-format songsheets

```python
from udn_songbook import SongBook
mybook = SongBook(inputs=['directory1', 'directory2', 'someotherfile.udn'])
```

Songbooks have an index auto-generated, and do not support mutiple songs with the same ID (which is
essentially "Title - Artist").

If your inputs include multiple songs in this way, the last one imported will be used. So name them
carefully.

A Songbook in this context is a collection of song objects with additional metadata, such as an
index.

## Tools

The pip package also installs 2 commandline tools, aimed at managing individual songsheets:

`udn_transpose`, which allows in-place (or optionally to a new file) transposing of an existing
songsheet by an arbitrary number of semitones. The transposition is added to metadata

`udn_songsheet`, which renders a UDN songsheet to a file in either PDF (default) or HTML format. it
also supports in-place transposition, without affecting the original input file.

## what you need to use this:

* a directory full of UDN-format files.
* templates:
  * index.html.j2
  * song.html.j2
* stylesheets (up to you, you can pass their names and location to the methods)
  * pdf.css
  * ukedown.css
