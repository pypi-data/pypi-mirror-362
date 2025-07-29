"""List of the GraceDB instances."""

from __future__ import annotations

import re
from enum import Enum
from typing import Any

from ligo.gracedb.rest import GraceDb

from .exceptions import MEGInvalidGraceDBAliasOrURLError

GRACEDB_URLS = {
    'production': 'https://gracedb.ligo.org',
    'playground': 'https://gracedb-playground.ligo.org',
    'test': 'https://gracedb-test.ligo.org',
    'dev': 'https://gracedb-test01.igwn.org',
    'cnaf': 'https://gracedb-test01.igwn.org',
    'local': 'https://gracedb.default.svc.cluster.local',
    'mocked': 'https://gracedb-donotexist.igwn.org',
}


class GraceDBWithContext(GraceDb):  # type: ignore[misc]
    """This class adds the URL and alias of the GranceDB server as attributes.

    The motivation of the meg_url attribute comes from the deprecation of GraceDb's
    service_url property.
    All the new attributes and methods are prefixed with 'meg_' to avoid potential
    future collision.
    """

    meg_url: str
    meg_alias: str | None
    MEG_URL_REGEX = re.compile(r'^https?://[A-Z0-9-.]+', re.I)

    def __init__(self, meg_url: str, meg_alias: str | None, **keywords: Any) -> None:
        """The GraceDBWithContext constructor."""
        super().__init__(**keywords)
        self.meg_url = meg_url
        self.meg_alias = meg_alias

    @classmethod
    def meg_from_alias_or_url(cls, value: str, **keywords: Any) -> GraceDBWithContext:
        """The GraceDBWithContext factory.

        Parameters:
            value: The GraceDB url, or an alias such as production, playground, etc.

        Raises:
            MEGInvalidGraceDBAliasOrURLError: When the specifier is not a known GraceDB
                alias nor a valid URL.
        """
        if value in GRACEDB_URLS:
            alias = value
            url = GRACEDB_URLS[value]
        elif cls.MEG_URL_REGEX.match(value):
            alias = None
            url = value
        else:
            raise MEGInvalidGraceDBAliasOrURLError(
                f'Invalid specifier for the GraceDB server: {value!r}. It should be a '
                f'URL or one of: {" ".join(GRACEDB_URLS)}',
            )
        return GraceDBWithContext(url, alias, service_url=f'{url}/api/', **keywords)


# XXX We should use StrEnum when mypy supports it: https://github.com/python/mypy/issues/11714  # noqa: E501
class GraceDBAlias(str, Enum):
    """Enum of the GraceDB instance names."""

    PRODUCTION = 'production'
    PLAYGROUND = 'playground'
    TEST = 'test'
    DEV = 'DEV'
    CNAF = 'cnaf'
    LOCAL = 'local'
    MOCKED = 'mocked'

    def __str__(self) -> str:
        """Value of the enum member."""
        return self.value
