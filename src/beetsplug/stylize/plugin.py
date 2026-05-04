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
from collections.abc import Callable
from functools import lru_cache
from typing import Literal
from typing import cast
from typing import get_args

import confuse
from beets import config
from beets.plugins import BeetsPlugin
from beets.util.color import CODE_BY_COLOR
from beets.util.color import COLOR_ESCAPE
from beets.util.color import RESET_COLOR


BeetsColor = Literal["auto", "always", "never"]


class StylizePlugin(BeetsPlugin):
    """Beets plugin to add style to your music library."""

    def __init__(self, name: str = "stylize", is_enabled: bool | None = None) -> None:
        super().__init__(name=name)

        self.template_funcs["link"] = self.link
        self.template_funcs["urlencode"] = self.urlencode

        if is_enabled is None:
            self.enabled = self.is_enabled()  # pragma: no cover
        else:
            self.enabled = is_enabled

        color: Callable[[str, str, str | None], str]
        nocolor: Callable[[str, str], str]
        if not self.enabled:

            def color(
                color_name: str, text: str, alternative: str | None = None
            ) -> str:
                if alternative is None:
                    return text
                else:
                    return alternative

            def nocolor(disabled: str, enabled: str = "") -> str:
                return disabled
        else:

            def color(
                color_name: str, text: str, alternative: str | None = None
            ) -> str:
                return self.stylize(color_name, text)

            def nocolor(disabled: str, enabled: str = "") -> str:
                return enabled

        self.template_funcs["stylize"] = color  # type: ignore[assignment]
        self.template_funcs["color"] = color  # type: ignore[assignment]
        self.template_funcs["nocolor"] = nocolor

    @staticmethod
    def is_enabled(
        beets_color: BeetsColor | None = None,
    ) -> bool:  # pragma: no cover
        """Check if color is enabled."""
        if beets_color is None:
            beets_color_str = os.environ.get("BEETS_COLOR", "auto")
            if beets_color_str not in get_args(BeetsColor):
                raise ValueError(
                    f"BEETS_COLOR must be {', '.join(get_args(BeetsColor))}"
                )
            beets_color = cast(BeetsColor, beets_color_str)

        return (
            bool(config["ui"]["color"].get(bool))
            and "NO_COLOR" not in os.environ
            and beets_color != "never"
            and (
                beets_color == "always"
                or (beets_color == "auto" and sys.stdout.isatty())
            )
        )

    def stylize(self, color_name: str, text: str) -> str:
        """Colorize text with a configured color (ui.colors)."""
        if text:
            code = self.color_codes(color_name)
            if code is None:
                return text
            else:
                code_str = ";".join(str(CODE_BY_COLOR[c]) for c in code)
                return f"{COLOR_ESCAPE}[{code_str}m{text}{RESET_COLOR}"
        else:
            return ""

    def link(self, url: str, link_text: str | None = None) -> str:
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
    def color_codes(color_name: str) -> list[str] | None:
        """Get configured color codes for a color name."""
        try:
            color_code: str = config["ui"]["colors"][color_name].get(str)
        except (confuse.ConfigTypeError, confuse.NotFoundError, NameError):
            # Normal color definition (type: list of unicode).
            try:
                color_code_list: list[str] = config["ui"]["colors"][color_name].get(
                    list
                )
            except (confuse.ConfigTypeError, confuse.NotFoundError, NameError):
                return None
        else:
            color_code_list = color_code.split()

        for code in color_code_list:
            if code not in CODE_BY_COLOR.keys():
                raise ValueError(f"no such ANSI code {code}")

        return color_code_list
