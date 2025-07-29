"""Component wrapper styles for prompt composition."""

from __future__ import annotations

from enum import Enum


class WrapperStyle(Enum):
    """Defines different wrapping styles for included components."""

    NONE = "none"
    XML = "xml"
    SEPARATOR = "separator"


def _apply_wrapper(content: str, component_name: str, style: WrapperStyle) -> str:
    """Apply a wrapper style to component content.

    Args:
        content: The component content to wrap
        component_name: The name of the component
        style: The wrapper style to apply

    Returns:
        The wrapped content
    """
    if style == WrapperStyle.NONE:
        return content
    elif style == WrapperStyle.XML:
        return f"<{component_name.upper()}>\n{content}\n</{component_name.upper()}>"
    elif style == WrapperStyle.SEPARATOR:
        separator = "-" * 12
        return f"{separator}\n" f"{content}\n" f"{separator}\n"
    else:
        return content
