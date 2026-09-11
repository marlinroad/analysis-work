#%%
from typing import Any

from IPython.display import Markdown, display


def display_report(*objects: Any, **kwargs: Any) -> Any:
    """Display report content using IPython's rich display system."""
    return display(*objects, **kwargs)


def display_header(text: str, level: int = 2) -> Any:
    """Display a Markdown heading."""
    if not 1 <= level <= 6:
        raise ValueError("Header level must be between 1 and 6.")

    return display_report(Markdown(f"{'#' * level} {text}"))