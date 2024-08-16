# Stylize Plugin for Beets

[![PyPI](https://img.shields.io/pypi/v/beets-stylize.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/beets-stylize.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/beets-stylize)][pypi status]
[![License](https://img.shields.io/pypi/l/beets-stylize)][license]

[![Read the documentation at https://beets-stylize.readthedocs.io/](https://img.shields.io/readthedocs/beets-stylize/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/kergoth/beets-stylize/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/kergoth/beets-stylize/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Ruff codestyle][ruff badge]][ruff project]

[pypi status]: https://pypi.org/project/beets-stylize/
[read the docs]: https://beets-stylize.readthedocs.io/
[tests]: https://github.com/kergoth/beets-stylize/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/kergoth/beets-stylize
[pre-commit]: https://github.com/pre-commit/pre-commit
[ruff badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
[ruff project]: https://github.com/charliermarsh/ruff

The `stylize` plugin adds three [template functions][] for use in [beets][] track and album listings. It is intended for use with the [format_item][] and [format_album][] configuration options. Using these functions will allow you to add style and color to the [list][] command and other commands that need to print out items.

- `stylize`: Add color and formatting to your formatted items and albums.
- `nocolor`: Show the supplied text only when color is disabled. This is useful to add separators between fields when color is unavailable.
- `link`: Create clickable links in the terminal. This has no effect on an unsupported terminal. This lets you play a track or navigate to an album folder with a click.

## Installation

As the beets documentation describes in [Other plugins][], to use an external plugin like this one, there are two options for installation:

- Make sure it’s in the Python path (known as `sys.path` to developers). This just means the plugin has to be installed on your system (e.g., with a setup.py script or a command like pip or easy_install). For example, `pip install beets-stylize`.
- Set the pluginpath config variable to point to the directory containing the plugin. (See Configuring) This would require cloning or otherwise downloading this repository before adding to the pluginpath.

## Configuring

First, enable the `stylize` plugin (see [Using Plugins][]). Colors for use with the `stylize` function may be defined using the [colors][] option under [UI Options][] in your beets configuration. For example:

```yaml
ui:
  colors:
    artist: ["bold", "green"]
```

## Using

The `stylize` function accepts a named color as the first argument, the text to be stylized as the second, and an optional third argument for the text to be used if color is disabled.

Example usage in your beets configuration, based on the default `format_item` and `format_album` configuration options:

```yaml
ui:
  color: true
  colors:
    # Field colors for use in the item and album formats.
    album: ["blue", "bold"]
    albumartist: ["yellow"]
    artist: ["bold", "yellow"]
    title: ["normal"]

format_item: "%stylize{artist,$artist} %nocolor{- }%stylize{album,$album} %nocolor{- }%stylize{title,$title}"
format_album: "%stylize{albumartist,$albumartist} %nocolor{- }%stylize{album,$album}"
```

With this configured, we see listings like this:

![Album Listing][]

And this:

![Track Listing][]

If no color is available, such as due to redirection, or setting the `NO_COLOR` environment variable, we see a listing like this due to the use of `%nocolor` to add the separator:

![Nocolor Listing][]

As an example of how to use `%link`, this would make the entire line a clickable link to the file path:

```yaml
format_item: "%link{file://$path,$artist - $album - $title}"
```

As we see here, in the Visual Studio Code terminal:

![Link Listing][]

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Stylize Plugin for Beets_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[template functions]: https://beets.readthedocs.io/en/stable/reference/pathformat.html#template-functions
[beets]: https://beets.readthedocs.io/en/stable/index.html
[format_item]: https://beets.readthedocs.io/en/stable/reference/config.html#id66
[format_album]: https://beets.readthedocs.io/en/stable/reference/config.html#id67
[list]: https://beets.readthedocs.io/en/stable/reference/cli.html#list-cmd
[other plugins]: https://beets.readthedocs.io/en/stable/plugins/index.html#other-plugins
[using plugins]: https://beets.readthedocs.io/en/stable/plugins/index.html#using-plugins
[colors]: https://beets.readthedocs.io/en/stable/reference/config.html#colors
[ui options]: https://beets.readthedocs.io/en/stable/reference/config.html#id81
[@cjolowicz]: https://github.com/cjolowicz
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/kergoth/beets-stylize/issues

<!-- github-only -->

[track listing]: ./docs/images/track_listing.png
[album listing]: ./docs/images/album_listing.png
[nocolor listing]: ./docs/images/nocolor_listing.png
[link listing]: ./docs/images/link_listing.png
[license]: https://github.com/kergoth/beets-stylize/blob/main/LICENSE
[contributor guide]: https://github.com/kergoth/beets-stylize/blob/main/CONTRIBUTING.md
