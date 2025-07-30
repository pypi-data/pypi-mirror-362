"""Time-based k-fold validation splits for heterogeneous data."""

import logging as _logging

from ._frontend import log_split_progress, plot, split

__all__ = [
    "__version__",  # Make MyPy happy
    "log_split_progress",
    "plot",
    "split",
]

__version__ = "0.7.0"

_logging.getLogger(__name__).addHandler(_logging.NullHandler())
