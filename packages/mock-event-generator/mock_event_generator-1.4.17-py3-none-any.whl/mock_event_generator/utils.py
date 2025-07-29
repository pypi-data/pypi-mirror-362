"""A simple tool to display trees.

From https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from pathlib import Path
from typing import Any, Callable

# prefix components:
SPACE = '    '
BRANCH = '│   '
# pointers:
TEE = '├── '
LAST = '└── '


def tree(
    dir_path: Path,
    criterion: Callable[[Path], bool] = lambda x: True,
    key: Callable[[Path], Any] | None = None,
    prefix: str = '',
) -> Iterator[tuple[Path, str]]:
    """A recursive generator to display a tree structure.

    Given a directory Path object it will yield a visual tree structure line by line
    with each line prefixed by the same characters.

    Parameters:
        dir_path: The directory to be displayed as a tree.
        criterion: Function that should return True to include the path in the tree.
        key: Function to sort the paths inside a given directory. By default, the
            alphanumerical order is used.
        prefix: Prefix to be prepended to the generated line.

    Yields:
        One line corresponding to a file or subdirectory contained in the specified
        path.
    """
    contents = sorted((_ for _ in dir_path.iterdir() if criterion(_)), key=key)
    # contents each get pointers that are ├── with a final └── :
    pointers = [TEE] * (len(contents) - 1) + [LAST]
    for pointer, path in zip(pointers, contents):
        yield path, prefix + pointer + path.name
        if path.is_dir():  # extend the prefix and recurse:
            extension = BRANCH if pointer == TEE else SPACE
            # i.e. space because last, └── , above so no more |
            yield from tree(path, criterion, key=key, prefix=prefix + extension)


SEVENT_REGEX = re.compile(r'M?S\d{5,}[a-z]+$')
GEVENT_REGEX = re.compile(r'[A-RT-Z]\d{4,}$')
GEVENT_REGEX1 = re.compile(r'Gev-\S{3,}$')


def is_gevent(event_id: str) -> bool:
    """Returns true if the identifier is that of a G-event.

    Paramters:
        event_id: The event identifier.
    """
    return bool(GEVENT_REGEX.match(event_id)) | bool(GEVENT_REGEX1.match(event_id))


def is_superevent(event_id: str) -> bool:
    """Returns true if the identifier is that of a superevent.

    A regular S-event identifier begins with `S`, a mock S-event with `MS`.

    Paramters:
        event_id: The event identifier.
    """
    return bool(SEVENT_REGEX.match(event_id))


def is_any_event(event_id: str) -> bool:
    """Returns true if the identifier is that of a G-event or S-event.

    Paramters:
        event_id: The event identifier.
    """
    return is_gevent(event_id) or is_superevent(event_id)


def split_filename(versioned_filename: str) -> tuple[str, int]:
    """Extract the file name and version from a versioned file.

    Parameters:
        versioned_filename: The input versioned file.

    Example:
        >>> split_filename('map.fits,3')
        ('map.fits', 3)
    """
    filename, version = versioned_filename.rsplit(',', 1)
    return filename, int(version)
