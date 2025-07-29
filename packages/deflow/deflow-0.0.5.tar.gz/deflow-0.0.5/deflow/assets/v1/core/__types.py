import re
from re import (
    IGNORECASE,
    UNICODE,
    VERBOSE,
    Pattern,
)


class Re:
    """Regular expression for parsing the group from filename."""

    __group_regex: str = r"""
        (?P<name>\w+)(?:\.(?P<tier>\w+))?(?:\.(?P<priority>\d+))
    """
    RE_GROUP: Pattern = re.compile(
        __group_regex, IGNORECASE | UNICODE | VERBOSE
    )
