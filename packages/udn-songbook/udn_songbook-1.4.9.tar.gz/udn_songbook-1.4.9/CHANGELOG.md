# CHANGELOG for udn_songbook

This project attempts to adhere to [semantic versioning](https://semver.org)

## 1.4.9
- still record unparseable chords
- support customisable chord types (qualities) in settings
- add UG conversion tool
- add UDN file parse testing tool
- disable transposition if any unknown chords 

## 1.4.8
- add new Song.udn() method to return UDN content as a string

## 1.4.7
- tidy up profile-specific inline CSS

## 1.4.6 type stubs
- adds py.typed marker
- refactors input type detection for Song objects
- raise TypeError for incorrect input types
- cleanup unused attributes
- reorder property declarations for readbility

## 1.4.5 Github Automations and other improvements
- move to dynamic tag-based versioning
- auto-publish on new tag (master only)
- auto-build on push (all branches)
- Add --index-only publishing option for testing
- make title_sort Title Case for sorting appropriately
- Keep punctuation in songid
- fix index columns css
- sort contents, use that to generate index
- Lots of CSS linting
- add stylelint configuration
- Add progress reporting to book pdf creator
- Support --destdir, use pathlib.Path
- Add tqdm for book generation tooling
- Add logging configuration to defaults
- log to file only in udn_songbook book.py
- Add .python-version
- singer names now bold uppercase for accessibility
- use the new load_settings function
- Handle empty YAML metadata (e.g. comments-only)

## 1.4.4 No idea how I missed out 1.4.3
- Add tag management (load/save)
- rename tooling such that udn_pdfbook -> tools/pdfbook.py
- clunky but working book building tool
- Fix footer links in song template for PDF output
- Fix index ID for links, support batching of entries
- Add output parameter to HTML method
- inputs and stylesheets are always lists.
- rename ukedown_elements to ukedown for simplicity
- use utils.renderer for jinja2 env in song.py


## 1.4.2
- Support custom settings files
- Add platformdirs to dependencies
- whitespace cleanup
- ruffiness
- removed requirements.txt
- updated annotations
- trailing whitespace

## 1.4.1 Stylesheets and profile updates
- support stylesheets in profile definitions
- support singers notes in template
- allow stylesheet overrides as parameters

## 1.4.0 Template updates
- patch version upgrade
- use list not typing.List
- Update templates to follow ukebook-md
- sync stylesheets with ukebook-md
- Add styling for repeat indicators


## 1.3.0
- Add dynaconf and profile support
- Docstrings everywhere
- move to pathlib whereever possible
- move to f-strings rather than str.format


## 1.2.0
- Add support for singers notes to template
- Add style (.singer) for singers' notes
- Docstringi, type hints and other linting updates
- Switch to ruff for python pre-commit, update versions
- remove unhelpful self._filename override
- Force normal font-style on elements inside backing vox

## 1.1.8

- Fix template for index generation
- Add latest CSS from ukebook-md
- Fix singers options in makesheet
- Unpunctuate song._index_entry for better sorting
- Rename default stylesheet to 'portrait.css'

## 1.1.7

- README updated with new udn_songbook.Song features

- BUGFIX: default metadata to empty dict if not present in songsheet
- BUGFIX: use absolute import for Song in transpose.py

## 1.1.6

- Adds README to project files for PyPi

## 1.1.5

- rename udn_render to udn_songsheet (script entry point)
- BUGFIX: stop wiping metadata after parsing songsheets

## 1.1.4

- support more than 100 songs in a songbook
- move tools into `udn_songbook/tools`
- new rendering tool
- update templates to support standalone songsheets (no footer links)
- BUGFIX: transpose no longer removes content after last chord.


## 1.1.3

- add scripts to project files
- add PDF rendering code
- move to pathlib.Path for filenames
- add `udn_transpose` entry point for transposing tool
- UNIX-safe chordnames
- template support for pychord.Chord objects

## 1.1.2

- dependency and documentation updates
- add license


## 1.1.1

- more sane boolean template vars
- new kwargs for templates (song & index)
- updated dependencies (new versions of blck/click/weasyprint etc)

## 1.1.0

- add page IDs
- adds rendering code & template for songs
- use pychord for chord naming
- add transposition code using pychord
- fix chord parsing to handle 'tails' like '*'
- page numbering and content deduplication

## 1.0.4

- require python >= 3.8

## 1.0.3

- dependency updates
  - Adds LXML dependency
  - python >= 3.7
- black-formatted
- adds pre-commit checks (black, flake8)
- adds index template

## 1.0.2

- update dependencies for PyYAML (5 or greater)

## 1.0.1

- update dependencies for newer versions of
  - BeautifulSoup4 4.9.3 to 5
  - ukedown v2-3
  - Markdown v3-4

## 1.0.0

- Initial Release (limited functionality)
- creates Song and SongBook objects from directories and files.
- Generates Index
