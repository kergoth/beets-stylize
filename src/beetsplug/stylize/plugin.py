"""Beets plugin to add style to your music library.

The plugin provides the following template plugins for path formats:

- `stylize`: Add color to your formatted items and albums.
- `nocolor`: Show the supplied text only when color is disabled.
- `link`: Create clickable links in the terminal.
"""

import os
import sys
from functools import lru_cache
from typing import List
from typing import Optional

import confuse  # type: ignore
from beets import config  # type: ignore
from beets.plugins import BeetsPlugin  # type: ignore
from beets.ui import ANSI_CODES  # type: ignore
from beets.ui import _colorize


class StylizePlugin(BeetsPlugin):  # type: ignore
    """Beets plugin to add style to your music library."""

    def __init__(self, name: str = "stylize") -> None:
        super().__init__(name=name)
        self.enabled = self.is_enabled()
        self.template_funcs["stylize"] = self.stylize
        self.template_funcs["nocolor"] = self.nocolor
        self.template_funcs["link"] = self.link

    def is_enabled(self) -> bool:
        """Check if color is enabled."""
        return (
            bool(config["ui"]["color"].get(True))
            and "NO_COLOR" not in os.environ
            and sys.stdout.isatty()
        )

    def stylize(
        self, color_name: str, text: str, alternative: Optional[str] = None
    ) -> str:
        """Colorize text with a configured color (ui.colors)."""
        if text:
            if self.enabled:
                code = self.color_codes(color_name)
                if code is None:
                    return text
                else:
                    return _colorize(code, text)  # type: ignore
            else:
                if alternative is None:
                    return text
                else:
                    return alternative
        else:
            return ""

    def nocolor(self, disabled_value: str, enabled_value: Optional[str] = None) -> str:
        """Return value if color is disabled."""
        if not self.enabled:
            return disabled_value
        else:
            return enabled_value or ""

    def link(self, url: str, link_text: Optional[str] = None) -> str:
        """Return a clickable link."""
        if link_text is None:
            link_text = url

        if (not os.getenv("NO_LINK")) and self.enabled:
            start = f"\033]8;;{url}\033\\"
            end = "\033]8;;\033\\"
            return f"{start}{link_text}{end}"
        else:
            return link_text

    @staticmethod
    @lru_cache
    def color_codes(color_name: str) -> Optional[List[str]]:
        """Get configured color codes for a color name."""
        try:
            color_code: str = config["ui"]["colors"][color_name].get(str)
        except (confuse.ConfigTypeError, confuse.NotFoundError, NameError):
            # Normal color definition (type: list of unicode).
            try:
                color_codes: List[str] = config["ui"]["colors"][color_name].get(list)
            except (confuse.ConfigTypeError, confuse.NotFoundError, NameError):
                return None
        else:
            color_codes = color_code.split()

        for code in color_codes:
            if code not in ANSI_CODES.keys():
                raise ValueError("no such ANSI code %s", code)

        return color_codes
