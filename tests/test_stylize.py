"""Tests for the 'stylize' plugin."""

import unittest

from beets import config  # type: ignore
from beets.test.helper import TestHelper  # type: ignore

from beetsplug import stylize


class BeetsTestCase(unittest.TestCase, TestHelper):  # type: ignore
    """TestHelper based TestCase for beets."""

    def setUp(self) -> None:
        """Set up test case."""
        self.setup_beets()

    def tearDown(self) -> None:
        """Tear down test case."""
        self.teardown_beets()


class StylizePluginTestCase(BeetsTestCase):
    """Base Class for the stylize beets plugin."""

    def setUp(self) -> None:
        """Set up test cases."""
        super().setUp()
        self.plugin = stylize.StylizePlugin(name="stylize", is_enabled=True)

    def _setup_config(self, **kwargs: str) -> None:
        """Set up configuration."""
        config["ui"]["colors"] = kwargs
        self.plugin.color_codes.cache_clear()


class StylizePluginTest(StylizePluginTestCase):
    """Test cases for the stylize beets plugin."""

    def test_color_notext(self) -> None:
        """Test stylize function with no text passed."""
        self._setup_config(color1="red")
        self.assertEqual(self.plugin.template_funcs["stylize"]("color1", ""), "")

    def test_color(self) -> None:
        """Test stylize function with color."""
        self._setup_config(color1="red", color2="green")
        self.assertEqual(
            self.plugin.template_funcs["stylize"]("color1", "foo"),
            "\x1b[31mfoo\x1b[39;49;00m",
        )
        self.assertEqual(
            self.plugin.template_funcs["stylize"]("color2", "bar"),
            "\x1b[32mbar\x1b[39;49;00m",
        )

    def test_undefined_color(self) -> None:
        """Test stylize function with undefined color."""
        self.assertEqual(self.plugin.template_funcs["stylize"]("color1", "foo"), "foo")

    def test_invalid_color_codes(self) -> None:
        """Test stylize function with invalid color codes."""
        self._setup_config(color1="foo")
        with self.assertRaises(ValueError) as cm:
            self.plugin.template_funcs["stylize"]("color1", "bar")
            self.assertEqual(str(cm.exception), "no such ANSI code foo")

    def test_nocolor(self) -> None:
        """Test nocolor function with style enabled."""
        self.assertEqual(self.plugin.template_funcs["nocolor"]("foo"), "")
        self.assertEqual(self.plugin.template_funcs["nocolor"]("foo", "bar"), "bar")

    def test_link(self) -> None:
        """Test link function."""
        self.assertEqual(
            self.plugin.link(
                "http://example.com",
                "foo",
            ),
            "\x1b]8;;http://example.com\x1b\\foo\x1b]8;;\x1b\\",
        )

    def test_link_no_text(self) -> None:
        """Test link function with no text."""
        self.assertEqual(
            self.plugin.link("http://example.com"),
            "\x1b]8;;http://example.com\x1b\\http://example.com\x1b]8;;\x1b\\",
        )

    def test_urlencode(self) -> None:
        """Test urlencode function."""
        self.assertEqual(
            self.plugin.urlencode("http://example.com?foo=bar"),
            "http%3A//example.com%3Ffoo%3Dbar",
        )

    def test_urlencode_notext(self) -> None:
        """Test urlencode function with no text."""
        self.assertEqual(self.plugin.urlencode(""), "")


class StylizePluginTestNoColor(StylizePluginTestCase):
    """Test cases for the stylize beets plugin with style disabled."""

    def setUp(self) -> None:
        """Set up test cases, disabling style."""
        super().setUp()
        self.plugin = stylize.StylizePlugin(name="stylize", is_enabled=False)

    def test_color_disabled(self) -> None:
        """Test stylize function with style disabled."""
        self._setup_config(color1="red")
        self.assertEqual(self.plugin.template_funcs["stylize"]("color1", "foo"), "foo")

    def test_color_alternative(self) -> None:
        """Test stylize function with color and alternative."""
        self._setup_config(color1="red")
        self.assertEqual(
            self.plugin.template_funcs["stylize"]("color1", "foo", "bar"), "bar"
        )

    def test_nocolor_disabled(self) -> None:
        """Test nocolor function with style disabled."""
        self.assertEqual(self.plugin.template_funcs["nocolor"]("foo"), "foo")
        self.assertEqual(self.plugin.template_funcs["nocolor"]("foo", "bar"), "foo")

    def test_link_disabled(self) -> None:
        """Test link function with style disabled."""
        self.assertEqual(
            self.plugin.link(
                "http://example.com",
                "foo",
            ),
            "foo",
        )
