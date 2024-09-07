"""Beets plugin to add style to your music library.

The plugin provides the following template plugins for path formats:

- `stylize` or `color`: Add color to your formatted items and albums.
- `nocolor`: Show the supplied text only when color is disabled.
- `link`: Create clickable links in the terminal.
- `urlencode`: URL-encode the supplied text.
"""

import os
import sys
import urllib.parse
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

    def __init__(
        self, name: str = "stylize", is_enabled: Optional[bool] = None
    ) -> None:
        super().__init__(name=name)

        self.template_funcs["link"] = self.link
        self.template_funcs["urlencode"] = self.urlencode

        if is_enabled is None:
            self.enabled = self.is_enabled()  # pragma: no cover
        else:
            self.enabled = is_enabled

        if not self.enabled:

            def color(
                color_name: str, text: str, alternative: Optional[str] = None
            ) -> str:
                if alternative is None:
                    return text
                else:
                    return alternative

            def nocolor(disabled: str, enabled: str = "") -> str:
                return disabled
        else:

            def color(
                color_name: str, text: str, alternative: Optional[str] = None
            ) -> str:
                return self.stylize(color_name, text)

            def nocolor(disabled: str, enabled: str = "") -> str:
                return enabled

        self.template_funcs["stylize"] = color
        self.template_funcs["color"] = color
        self.template_funcs["nocolor"] = nocolor

    def is_enabled(self) -> bool:  # pragma: no cover
        """Check if color is enabled."""
        return (
            bool(config["ui"]["color"].get(True))
            and "NO_COLOR" not in os.environ
            and sys.stdout.isatty()
        )

    def stylize(self, color_name: str, text: str) -> str:
        """Colorize text with a configured color (ui.colors)."""
        if text:
            code = self.color_codes(color_name)
            if code is None:
                return text
            else:
                return _colorize(code, text)  # type: ignore
        else:
            return ""

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

    def urlencode(self, link_text: str = "") -> str:
        """Return URL encoded link_text."""
        return urllib.parse.quote(link_text)

    @staticmethod
    @lru_cache
    def color_codes(color_name: str) -> Optional[List[str]]:
        """Get configured color codes for a color name."""
        try:
            color_code: str = config["ui"]["colors"][color_name].get(str)
        except (confuse.ConfigTypeError, confuse.NotFoundError, NameError):
            # Normal color definition (type: list of unicode).
            try:
                color_code_list: List[str] = config["ui"]["colors"][color_name].get(
                    list
                )
            except (confuse.ConfigTypeError, confuse.NotFoundError, NameError):
                return None
        else:
            color_code_list = color_code.split()

        for code in color_code_list:
            if code not in ANSI_CODES.keys():
                raise ValueError("no such ANSI code %s", code)

        return color_code_list
