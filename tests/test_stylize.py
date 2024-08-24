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


class StylizePluginTest(BeetsTestCase):
    """Test cases for the stylize beets plugin."""

    def setUp(self) -> None:
        """Set up test cases."""
        super().setUp()
        self.plugin = stylize.StylizePlugin()
        self.plugin.enabled = True

    def _setup_config(self, **kwargs: str) -> None:
        """Set up configuration."""
        config["ui"]["colors"] = kwargs
        self.plugin.color_codes.cache_clear()

    def test_color_notext(self) -> None:
        """Test stylize function with no text passed."""
        self._setup_config(color1="red")
        self.assertEqual(self.plugin.stylize("color1", ""), "")

    def test_color(self) -> None:
        """Test stylize function with color."""
        self._setup_config(color1="red", color2="green")
        self.assertEqual(
            self.plugin.stylize("color1", "foo"), "\x1b[31mfoo\x1b[39;49;00m"
        )
        self.assertEqual(
            self.plugin.stylize("color2", "bar"), "\x1b[32mbar\x1b[39;49;00m"
        )

    def test_color_disabled(self) -> None:
        """Test stylize function with color disabled."""
        self.plugin.enabled = False
        self._setup_config(color1="red")
        self.assertEqual(self.plugin.stylize("color1", "foo"), "foo")
        self.plugin.enabled = True

    def test_color_alternative(self) -> None:
        """Test stylize function with color and alternative."""
        self.plugin.enabled = False
        self._setup_config(color1="red")
        self.assertEqual(self.plugin.stylize("color1", "foo", "bar"), "bar")
        self.plugin.enabled = True

    def test_undefined_color(self) -> None:
        """Test stylize function with undefined color."""
        self.assertEqual(self.plugin.stylize("color1", "foo"), "foo")

    def test_invalid_color_codes(self) -> None:
        """Test stylize function with invalid color codes."""
        self._setup_config(color1="foo")
        with self.assertRaises(ValueError) as cm:
            self.plugin.stylize("color1", "bar")
            self.assertEqual(str(cm.exception), "no such ANSI code foo")

    def test_nocolor(self) -> None:
        """Test nocolor function."""
        self.assertEqual(self.plugin.nocolor("foo"), "")
        self.assertEqual(self.plugin.nocolor("foo", "bar"), "bar")

        self.plugin.enabled = False
        self.assertEqual(self.plugin.nocolor("foo"), "foo")
        self.assertEqual(self.plugin.nocolor("foo", "bar"), "foo")
        self.plugin.enabled = True

    def test_link(self) -> None:
        """Test link function."""
        self.assertEqual(
            self.plugin.link(
                "http://example.com",
                "foo",
            ),
            "\x1b]8;;http://example.com\x1b\\foo\x1b]8;;\x1b\\",
        )

    def test_link_disabled(self) -> None:
        """Test link function with link disabled."""
        self.plugin.enabled = False
        self.assertEqual(
            self.plugin.link(
                "http://example.com",
                "foo",
            ),
            "foo",
        )
        self.plugin.enabled = True

    def test_link_no_text(self) -> None:
        """Test link function with no text."""
        self.assertEqual(
            self.plugin.link("http://example.com"),
            "\x1b]8;;http://example.com\x1b\\http://example.com\x1b]8;;\x1b\\",
        )
