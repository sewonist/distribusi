# Distribusi CMS

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

## Installation

Using [--user] or [a virtual environment] is recommended:

[--user]: https://packaging.python.org/tutorials/installing-packages/#installing-to-the-user-site
[a virtual environment]: https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments


```bash
$ pip install --user distribusi
```

## Usage

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

Install [Pipenv] and then run:

[Pipenv]: https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv

```
$ pipenv install --dev
$ pipenv run pip install -e .
$ pipenv run distribusi --help
```


## Release It

```
$ make publish
```
