from enum import Enum, IntEnum


class LogPrefixes(Enum):
    RUNNING = '[~]'
    QUESTION = '[?]'
    BAD = '[-]'
    GOOD = '[+]'
    WARNING = '[!]'
    ERROR = '[*]'
    CRITICAL = '[X]'


class SysExits(IntEnum):
    # https://sites.uclouvain.be/SystInfo/usr/include/sysexits.h.html

    OK = 0
    USAGE = 64  # Command Line Usage
    DATAERR = 65  # Data format error
    NOINPUT = 66  # Could not open input
    NOUSER = 67  # Addressee not found
    NOHOST = 68  # Could not find hostname
    UNAVAILABLE = 69  # Service unavailable
    SOFTWARE = 70  # Software error
    OSERR = 71  # System error (fork issues, etc)
    OSFILE = 72  # Critical OS file missing
    CANTCREATE = 73  # Can't create new file
    IOERR = 74  # I/O error
    TEMPFAIL = 75  # Try again
    PROTOCOL = 76  # Protocol error
    NOPERM = 77  # Permission denied
    CONFIG = 78  # Configuration error
