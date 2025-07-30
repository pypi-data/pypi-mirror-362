"""Supporting functions for the Streamlit companion app.

The app may be installed by running ``pip install time-split[app]``. The application API is *not* stable, but will be
available under the ``time_split_app`` namespace. Repo: https://github.com/rsundqvist/time-split-app/.
"""

from ._create_explorer_link import create_explorer_link

__all__ = [
    "create_explorer_link",
]
