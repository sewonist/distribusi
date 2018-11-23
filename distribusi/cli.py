import argparse

from distribusi.distribusi import distribusify


def build_argparser():
    parser = argparse.ArgumentParser("""
    distbusi is a content management system for the web that produces static
    index pages based on folders in the filesystem. It is inspired by the
    automatic index functions featured in several web servers. It works by
    traversing the file system and directory hierarchy to automatically list
    all the files in the directory and providing them with html classes and
    tags for easy styling.
    """)

    parser.add_argument(
        '-d',
        '--directory',
        help="Select which directory to distribute"
    )

    parser.add_argument(
        '-v',
        '--verbose',
        help="Print verbose debug output",
        action="store_true"
    )

    parser.add_argument(
        '-t',
        '--thumbnail',
        help="Generate 150x150 thumbnails for images",
        action="store_true"
    )

    parser.add_argument(
        '-n',
        '--no-template',
        help="Don't use the template to ouput html",
        action="store_true"
    )

    return parser


def cli_entrypoint():
    parser = build_argparser()
    args = parser.parse_args()

    if args.directory:
        if args.verbose:
            print('Generating directory listing for', args.directory)
        if args.thumbnail:
            print('Making thumbnails')
            directory = args.directory
    else:
        directory = '.'

    distribusify(args, directory)
