# agesafetch

[![crates.io Version][Version Badge]][crates.io]
[![crates.io Downloads][Downloads Badge]][crates.io]
[![License: MIT][License Badge]][LICENSE]
[![REUSE Status][REUSE Badge]][REUSE Status]

[crates.io]: https://crates.io/crates/agesafetch
[Version Badge]: https://img.shields.io/crates/v/agesafetch
[Downloads Badge]: https://img.shields.io/crates/d/agesafetch
[License Badge]: https://img.shields.io/gitlab/license/BVollmerhaus%2Fagesafetch
[REUSE Status]: https://api.reuse.software/info/gitlab.com/BVollmerhaus/agesafetch
[REUSE Badge]: https://api.reuse.software/badge/gitlab.com/BVollmerhaus/agesafetch

A tool for obtaining your firmware's embedded [AGESA] version on Linux.

[AGESA]: https://en.wikipedia.org/wiki/AGESA

## Installation

[![AUR Version][AUR Badge]][AUR Package]
[![PyPI Version][PyPI Badge]][PyPI Package]

[AUR Package]: https://aur.archlinux.org/packages/agesafetch
[AUR Badge]: https://img.shields.io/aur/version/agesafetch
[PyPI Package]: https://pypi.org/project/agesafetch/
[PyPI Badge]: https://img.shields.io/pypi/v/agesafetch

### Binaries

Pre-compiled and signed binaries are provided with all [GitLab releases].

[GitLab releases]: https://gitlab.com/BVollmerhaus/agesafetch/-/releases

### From Source

```shell
cargo install agesafetch
```

#### Note

By default, Cargo installs binaries in `~/.cargo/bin`, so that directory
must be in `$PATH` for `agesafetch` to be found. However, not all methods
of privilege escalation preserve the `$PATH` variable, e.g. _sudo_ with a
`secure_path` value.

When in doubt, refer to the complete path: `sudo ~/.cargo/bin/agesafetch`

### From PyPI

```shell
sudo pipx install --global agesafetch
# or, to run it directly without a persistent installation:
sudo pipx run agesafetch
```

#### Python Bindings

On top of the `agesafetch` command, the Python package also provides basic
bindings for the AGESA search that you can invoke from your own code (which
then also requires elevated privileges or capabilities):

```python
import agesafetch

version: agesafetch.AGESAVersion | None = agesafetch.find_agesa_version()
```

## Usage

```shell
agesafetch [-h]
```

<sup>
  🔒 The AGESA search requires elevated privileges or suitable capabilities.
</sup>

Simply run `agesafetch` to invoke a search for the AGESA version in memory:

```shell
$ sudo agesafetch
:: Searching Reserved region #1 (1667 KiB)...
-> Found AGESA version: CezannePI-FP6 1.0.1.1
```

When run non-interactively, such as in pipes or redirections, `agesafetch`
will automatically suppress all output except for the found version:

```shell
$ sudo agesafetch > found_version
$ cat found_version
CezannePI-FP6 1.0.1.1
```

## Testing

agesafetch has been confirmed to work on a broad set of systems, including:

* ASUS X670E and X870E desktop boards
* Gigabyte B450, B550, B650, and X570 boards
* Multiple Lenovo ThinkPad P14s Gen 1 & 2 AMD
* An assortment of EPYC-based server platforms

See [Tested Platforms] for the complete list. If you tested agesafetch on a
new system and would like to add it, please get in touch!

[Tested Platforms]: https://gitlab.com/BVollmerhaus/agesafetch/blob/master/docs/tested-platforms.md

## Author

* [Benedikt Vollmerhaus](https://gitlab.com/BVollmerhaus)

## Thanks To

* [Matthias Bräuer], for testing and code reviews.
* [Tan Siewert], for extensive testing using EPYC.

[Matthias Bräuer]: https://gitlab.com/Braeuer
[Tan Siewert]: https://gitlab.com/sinuscosinustan

## License

This project is licensed under the MIT license. See the [LICENSE] file for
more information.

[LICENSE]: https://gitlab.com/BVollmerhaus/agesafetch/blob/master/LICENSE
