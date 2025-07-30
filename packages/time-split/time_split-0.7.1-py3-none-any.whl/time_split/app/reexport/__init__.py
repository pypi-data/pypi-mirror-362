"""Reexported resources from the ``time_split_app`` namespace.

Running ``python -m time_split app new`` will create a ``Dockerfile`` and a simple ``my_extensions.py`` module.

Environment variables:
    Subset of variables used to customize Docker-based deployments.

    .. envvar:: DATASET_LOADER

       A :class:`DataLoaderWidget` instance or type, e.g. ``my_extensions:MyDatasetLoader``.

    .. envvar:: SPLIT_SELECT_FN

       A :attr:`SelectSplitParams`-function, e.g. ``my_extensions:my_select_fn``.

    .. envvar:: PLOT_FN

       A :func:`~time_split.plot`-like function, e.g. ``my_extensions:my_plot_fn``.

    .. envvar:: LINK_FN

       A :func:`.create_explorer_link`-like function, e.g. ``my_extensions:my_link_fn``.

    See https://github.com/rsundqvist/time-split-app/blob/master/src/time_split_app/config.py
    for more variable-based configuration options.
"""

from time_split_app.datasets import Dataset, DatasetConfig, DuplicateIndexError, load_dataset, load_dataset_configs
from time_split_app.widgets import DataLoaderWidget, DurationWidget, select_datetime, select_duration
from time_split_app.widgets import types as _types
from time_split_app.widgets.types import QueryParams

SelectSplitParams = _types.SelectSplitParams
"""Type of :envvar:`SPLIT_SELECT_FN`.

A callable ``() -> split_params``; see :func:`time_split.split`
and :attr:`~time_split.types.DatetimeIndexSplitterKwargs`.
"""
PlotFn = _types.PlotFn
"""Type of :envvar:`PLOT_FN`."""
LinkFn = _types.LinkFn
"""Type of :envvar:`LINK_FN`."""

__all__ = [
    "DataLoaderWidget",
    "Dataset",
    "DatasetConfig",
    "DuplicateIndexError",
    "DurationWidget",
    "LinkFn",
    "PlotFn",
    "QueryParams",
    "SelectSplitParams",
    "load_dataset",
    "load_dataset_configs",
    "select_datetime",
    "select_duration",
]
