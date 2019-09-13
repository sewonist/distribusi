# Distribusi CMS

[![PyPI version](https://badge.fury.io/py/distribusi.svg)](https://badge.fury.io/py/distribusi)

`distribusi` is a content management system for the web that produces static
index pages based on folders in the filesystem. It is inspired by the automatic
index functions featured in several web servers. It works by traversing the
file system and directory hierarchy to automatically list all the files in the
directory and providing them with html classes and tags for easy styling.

## Requirements

While a Pip install will pull in Python dependencies, you might need system
dependencies. This package requires two underlying packages. Those are
`python-magic`, and `pillow`. Here are the installation documentation for those
packages:

* [github.com/threatstack/libmagic](https://github.com/threatstack/libmagic)
* [pillow.readthedocs.io](https://pillow.readthedocs.io/en/5.3.x/installation.html#external-libraries)

### Optional requirements

If you wish to use the `--caption` flag to add image captions read from EXIF comment metadata you will need a utility called `exiftool`.

You can install it via your package manager. For other options please consult the website: [https://www.sno.phy.queensu.ca/~phil/exiftool/](https://www.sno.phy.queensu.ca/~phil/exiftool/)


## Install It

```bash
$ export PATH=$PATH:$HOME/.local/bin
$ pip install --user distribusi
```

## Upgrade It

If you already have it, you can upgrade with:

```bash
$ pip install -U distribusi
```

## Use It

Get help with:

```bash
$ distribusi --help
```

Make a distribusi of your home folder:

```bash
$ distribusi -d ~/
```

You will find that you now have an `index.html` in every folder.

Create a quick gallery for the web:

```
$ distribusi -d /path/to/my/photos -t
```

This creates an `index.html` with `base64` encoded thumbnails.

Generate verbose output:

```
$ distribusi -v
```

Make an index of the archive page:

```
$ distribusi -d /var/www/archive/my_event -t -v
```

# ✌

## Change It

You'll need to get a copy of the repository and then do an [editable] install:

[editable]: https://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode

```bash
$ git clone https://git.vvvvvvaria.org/varia/distribusi.git && cd distribusi
$ python3 -m venv .venv && source .venv/bin/activate
$ pip install -e .
```

You're then ready to make your changes and experiment with them.

## Release It

You'll need a [PyPi](https://pypi.org/) account and to be added as a maintainer.

Please ask around @ Varia for who has PyPi access.

```
$ pip install twine
$ make publish
```
