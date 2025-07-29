# filters.py
# additional jinja2 filters used by the songbook rendering engine


def safe_name(chord):
    """
    Makes chordnames 'safe' (no shell special chars)
    Might need expanding for Windows/Mac)

    Args:
        chord(str): a chordname to manipulate

    Returns:
        str: chordname with awkward characters replaced
    """
    # rules:
    # replace '#' with _sharp if at end,
    #                   _sharp_ if not
    # replace '/' with _on_
    return chord.translate({ord("#"): "_sharp_", ord("/"): "_on_"})


def chunk(iterable, chunksize):
    """
    iterate over an iterable, returning chunks of size (length) chunksize.
    Any remainder is returned as the last chunk.

    Essentially walk over an iterable in batches of `chunksize`

    Args:
        iterable: any iterable object (list, str, dict etc)
        chunksize(int): size of chunks to return

    """
    for i in range(0, len(iterable), chunksize):
        yield (iterable[i : i + chunksize])


custom_filters = {"safe_name": safe_name, "chunk": chunk}
