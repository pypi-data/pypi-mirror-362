"""Constructors for os file errors."""

import errno
import os


def not_found(location):
    """Create a FileNotFoundError."""
    return FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), str(location))


def exists(location):
    """Create a FileExistsError."""
    return FileExistsError(errno.EEXIST, os.strerror(errno.EEXIST), str(location))


def is_dir(location):
    """Create a IsADirectoryError."""
    return IsADirectoryError(errno.EISDIR, os.strerror(errno.EISDIR), str(location))


def not_dir(location):
    """Create a NotADirectoryError."""
    return NotADirectoryError(errno.ENOTDIR, os.strerror(errno.ENOTDIR), str(location))
