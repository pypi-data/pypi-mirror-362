"""
This package defines a Python interface for installing, managing, querying,
and performing other operations on Zeek Packages and Package Sources.
The main entry point is the :class:`Manager <zeekpkg.manager.Manager>` class.

This package provides a logger named ``LOG`` to which logging stream handlers
may be added in order to help log/debug applications.
"""

import logging

__version__ = "3.1.0"
__all__ = ["manager", "package", "source", "template", "uservar"]  # noqa: F405

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())

from .manager import *  # noqa: F403
from .package import *  # noqa: F403
from .source import *  # noqa: F403
from .uservar import *  # noqa: F403
