"""Beets plugin to add style to your music library.

The plugin provides the following template plugins for path formats:

- `stylize`: Add color to your formatted items and albums.
- `nocolor`: Show the supplied text only when color is disabled.
- `link`: Create clickable links in the terminal.
"""

import os
import sys
from typing import List
from typing import Optional

import confuse
from beets import config
from beets.plugins import BeetsPlugin
from beets.ui import ANSI_CODES
from beets.ui import UserError
from beets.ui import _colorize


class StylizePlugin(BeetsPlugin):
    """Beets plugin to add style to your music library."""

    def __init__(self) -> None:
        super().__init__()
        self.stylize_enabled = self.enabled()
        self.template_funcs["stylize"] = self.stylize
        self.template_funcs["nocolor"] = self.nocolor
        self.template_funcs["link"] = self.link
        self.color_codes = FactoryDict(self.lookup_color_codes)

    def enabled(self) -> bool:
        """Check if color is enabled."""
        return (
            config["ui"]["color"]
            and "NO_COLOR" not in os.environ
            and sys.stdout.isatty()
        )

    def stylize(self, color_name: str, text: str, alternative: Optional[str] = None):
        """Colorize text with a configured color (ui.colors)."""
        if text:
            if self.stylize_enabled:
                color_codes = self.color_codes[color_name]
                return _colorize(color_codes, text)
            else:
                if alternative is None:
                    return text
                else:
                    return alternative
        else:
            return ""

    def nocolor(self, disabled_value: str, enabled_value: Optional[str] = None):
        """Return value if color is disabled."""
        if not self.stylize_enabled:
            return disabled_value
        else:
            return enabled_value or ""

    def link(self, url: str, link_text: Optional[str] = None):
        """Return a clickable link."""
        if link_text is None:
            link_text = url

        if (not os.getenv("NO_LINK")) and self.stylize_enabled:
            start = f"\033]8;;{url}\033\\"
            end = "\033]8;;\033\\"
            return f"{start}{link_text}{end}"
        else:
            return link_text

    def lookup_color_codes(self, color_name: str) -> List[str]:
        """Get configured color codes for a color name."""
        try:
            color_def = config["ui"]["colors"][color_name].get(str)
        except (confuse.ConfigTypeError, NameError):
            # Normal color definition (type: list of unicode).
            try:
                color_def = config["ui"]["colors"][color_name].get(list)
            except (confuse.ConfigTypeError, NameError) as exc:
                raise UserError("no such color %s", color_def) from exc
        else:
            color_def = color_def.split()

        for code in color_def:
            if code not in ANSI_CODES.keys():
                raise ValueError("no such ANSI code %s", code)

        return color_def


class FactoryDict(dict):
    """Call a factory function to populate on demand, caching it in the dict."""

    def __init__(self, factory, iterable=None, **kwargs):
        if iterable is not None:
            super().__init__(iterable)
        else:
            super().__init__(**kwargs)
        self.factory = factory

    def __missing__(self, key):
        """Populate the dict with the factory function."""
        self[key] = value = self.factory(key)
        return value
