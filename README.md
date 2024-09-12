# Stylize Plugin for Beets

[![PyPI](https://img.shields.io/pypi/v/beets-stylize.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/beets-stylize.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/beets-stylize)][pypi status]
[![License](https://img.shields.io/pypi/l/beets-stylize)][license]

[![Read the documentation at https://beets-stylize.readthedocs.io/](https://img.shields.io/readthedocs/beets-stylize/latest.svg?label=Read%20the%20Docs)][read the docs]
[![The Ethical Source Principles](https://img.shields.io/badge/ethical-source-%23bb8c3c?labelColor=393162)][ethical source]
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)][contributor covenant]
[![Tests](https://github.com/kergoth/beets-stylize/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/kergoth/beets-stylize/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Ruff codestyle][ruff badge]][ruff project]

[pypi status]: https://pypi.org/project/beets-stylize/
[ethical source]: https://ethicalsource.dev/principles/
[read the docs]: https://beets-stylize.readthedocs.io/
[tests]: https://github.com/kergoth/beets-stylize/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/kergoth/beets-stylize
[pre-commit]: https://github.com/pre-commit/pre-commit
[ruff badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
[ruff project]: https://github.com/charliermarsh/ruff

![Album Listing][]

The [stylize](https://github.com/kergoth/beets-stylize) plugin adds style and color to the [list][] command and other commands that need to print out items, by adding three [template functions][] for use with the [format_item][] and [format_album][] configuration options.

- `stylize` or `color`: Add color and formatting to your formatted items and albums.
- `nocolor`: Show the supplied text only when color is disabled. This is useful to add separators between fields when color is unavailable.
- `link`: Create clickable links in the terminal. This has no effect on an unsupported terminal. This lets you play a track or navigate to an album folder with a click.
- `urlencode`: URL-encode the supplied text.

## Installation

As the beets documentation describes in [Other plugins][], to use an external plugin like this one, there are two options for installation:

- Make sure it’s in the Python path (known as `sys.path` to developers). This just means the plugin has to be installed on your system (e.g., with a setup.py script or a command like pip or easy_install). For example, `pip install beets-stylize`.
- Set the pluginpath config variable to point to the directory containing the plugin. (See Configuring) This would require cloning or otherwise downloading this [repository](https://github.com/kergoth/beets-stylize) before adding to the pluginpath.

## Configuring

First, enable the `stylize` plugin (see [Using Plugins][]). Colors for use with the `stylize` function may be defined using the [colors][] option under [UI Options][] in your beets configuration. For example:

```yaml
ui:
  colors:
    artist: ["bold", "green"]
```

## Using

The `stylize` function accepts a named color as the first argument, the text to be stylized as the second, and an optional third argument for the text to be used if color is disabled.

### Example Usage

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

### Example Usage From My Personal Configuration

![Personal Config Listings][]

This example is more elaborate, and includes usage of [alias][], [savedformats][], [inline][] and [albumtypes][]. [alias][] is only used to provide separate commands that use `%link`, as using it seems to have a performance impact, so I don't want it always used. [savedformats][] is only used to split up the default format strings for readability and maintainability, but is not required. [inline][] can be used instead of [savedformats][] to provide the `icon` field.

```yaml
plugins: stylize alias savedformats inline albumtypes

aliases:
  lsl:
    help: List items, linking to their files
    command: ls -f '%link{file://$path,$icon} $format_item'
    aliases: list-linked

  lsf:
    help: List items, with links to play them in foobar2000 (macOS only)
    command: ls -f '%link{shortcuts://run-shortcut?name=Open in foobar2000&input=text&text=%urlencode{$path},$icon} $format_item'
    aliases: list-foobar2k

item_fields:
  icon: '"📄"'
  disc_and_track: |
    if not track or (tracktotal and tracktotal == 1):
      return ''
    elif disctotal > 1:
      return u'%02i.%02i' % (disc, track)
    else:
      return u'%02i' % track

album_fields:
  icon: '"📁"'

item_formats:
  format_item: "%ifdef{id,$format_id }%if{$singleton,,$format_album_title %nocolor{| }}$format_year %nocolor{- }$format_track"

  format_id: "%stylize{id,$id,[$id]}"
  format_album_title: "%stylize{album,$album%aunique{}}%if{$albumtypes,%stylize{albumtypes,%ifdef{atypes,%if{$atypes, $atypes}}}}"
  format_year: "%stylize{year,$year}"

  format_track: "%if{$singleton,,%if{$disc_and_track,$format_disc_and_track %nocolor{- }}}$format_artist$format_title"
  format_disc_and_track: "%stylize{track,$disc_and_track}"
  format_artist: "%stylize{artist,$artist} %nocolor{- }"
  format_title: "%stylize{title,$title}"

album_formats:
  format_album: "%ifdef{id,$format_album_id }%if{$albumartist,$format_albumartist %nocolor{- }}$format_album_title %nocolor{| }$format_year"

  format_album_id: "%stylize{id,$id,[$id]}"
  format_albumartist: "%stylize{albumartist,$albumartist}"
  format_album_title: "%stylize{album,$album%aunique{}}%if{$albumtypes,%stylize{albumtypes,%ifdef{atypes,%if{$atypes, $atypes}}}}"
  format_year: "%stylize{year,$year}"

  # Allow for aliases with `-f '$format_item'` to be used when `-a` is passed
  format_item: "$format_album"

format_album: "$format_album"
format_item: "$format_item"

ui:
  colors:
    album: ["blue", "bold"]
    albumartist: ["yellow", "bold"]
    albumtypes: ["cyan"]
    artist: ["yellow", "bold"]
    id: ["faint"]
    title: ["normal"]
    track: ["green"]
    year: ["magenta", "bold"]
```

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Stylize Plugin for Beets_ is free and open source software. This software prioritizes meeting the criteria of the [Ethical Source Principles][ethical source], though it does not currently utilize an [ethical source license][].

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project is a plugin for the [beets][] project, and would not exist without that fantastic project.
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
[ethical source license]: https://ethicalsource.dev/faq/#what-is-an-ethical-license-for-open-source
[file an issue]: https://github.com/kergoth/beets-stylize/issues
[alias]: https://github.com/kergoth/beets-alias
[savedformats]: https://github.com/kergoth/beets-kergoth/blob/master/docs/savedformats.rst
[inline]: https://beets.readthedocs.io/en/stable/plugins/inline.html
[albumtypes]: https://beets.readthedocs.io/en/stable/plugins/albumtypes.html

<!-- github-only -->

[track listing]: ./docs/images/track_listing.png
[album listing]: ./docs/images/album_listing.png
[nocolor listing]: ./docs/images/nocolor_listing.png
[link listing]: ./docs/images/link_listing.png
[personal config listings]: ./docs/images/my_config_listings.png
[license]: ./LICENSE
[contributor guide]: ./CONTRIBUTING.md
[contributor covenant]: ./CODE_OF_CONDUCT.md
