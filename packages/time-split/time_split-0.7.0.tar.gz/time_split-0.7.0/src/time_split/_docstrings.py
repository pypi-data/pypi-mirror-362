from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


def add_docstrings(**kwargs: str) -> None:
    """Add a documented argument to the ``@docs`` decorator."""
    _DOCSTRINGS.update(kwargs)


def docs(__func: Callable[P, T], /) -> Callable[P, T]:
    """Add info the docstring of a function."""
    assert __func.__doc__ is not None  # noqa: S101
    __func.__doc__ = __func.__doc__.format(**_DOCSTRINGS)
    return __func


_OFFSET = "pandas :ref:`offset alias <pandas:timeseries.offset_aliases>`"
_SPAN = (
    f"Range {{arg}} `schedule` timestamps. Either a {_OFFSET}, an integer (`schedule`-based offsets), "
    f"or `'all'` (requires `available` data)."
)
_DOCSTRINGS = {
    "schedule": f"A :attr:`~time_split.types.DatetimeIterable`, {_OFFSET}, or `cron <https://pypi.org/project/croniter/>`_ expression.",
    "before": _SPAN.format(arg="before"),
    "after": _SPAN.format(arg="after"),
    "step": "Select a subset of folds, preferring folds later in the schedule.",
    "n_splits": "Maximum number of folds, preferring folds later in the schedule.",
    "available": "Binds `schedule` to a range.",
    "expand_limits": f'A {_OFFSET} used to expand `available` data to its likely `"true"` limits. Pass ``False`` to disable.',
    "ignore_filters": "Set to ignore filtering parameters (e.g. `step`) and global configuration.",
    "USER_GUIDE": (
        "For more information about the `schedule`, `before/after` and `expand_limits`-arguments"
        ", see the :ref:`User guide`."
    ),
    "OFFSET": _OFFSET,
    "DatetimeIndexSplitterKwargs": "See :func:`~time_split.split`. The `available` keyword is managed by the integration.",
    "show_removed": "If ``True``, splits removed by `n_splits` or `step` are included in the figure.",
}
