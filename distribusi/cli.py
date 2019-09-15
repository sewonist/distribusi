import argparse
import os

from distribusi.distribusi import distribusify


def build_argparser():
    parser = argparse.ArgumentParser("""
    distbusi is a content management system for the web that produces static
    index pages based on folders in the files system.
    It is inspired by the automatic index functions featured in several popular web
    servers. distribusi works by traversing the file system and directory hierarchy
    to automatically list all the files in the directory, detect the file types and
    providing them with relevant html classes and tags for easy styling.""")

    parser.add_argument(
        '-d', '--directory', help="Select which directory to distribute", default="."
    )

    parser.add_argument(
        '-s', '--style', help="Select a CSS style sheet to include"
    )

    parser.add_argument(
        '-v', '--verbose', help="Print verbose debug output", action="store_true"
    )

    parser.add_argument(
        '-t',
        '--thumbnail',
        help="Generate 450x450 thumbnails for images",
        action="store_true",
    )

    parser.add_argument(
        '-n',
        '--no-template',
        help="Don't use the template to output html",
        action="store_true",
    )

    parser.add_argument(
        '-nf',
        '--no-filenames',
        help="Don't add file names to listing",
        action="store_true",
    )

    parser.add_argument(
        '-c',
        '--captions',
        help="Adds image captions based on EXIF metadata, requires 'exiftool'",
        action="store_true",
    )

    parser.add_argument(
        '-r',
        '--remove-index',
        help="Recursively removes all instances of index.html that have been previously made by distribusi",
        action="store_true")

    parser.add_argument(
        '-e',
        '--exclude-directory',
        help="Exclude one or multiple directories from indexing",
        nargs="*",
        metavar='DIR'
        )

    return parser


def cli_entrypoint():
    parser = build_argparser()
    args = parser.parse_args()
    distribusify(args, args.directory)
