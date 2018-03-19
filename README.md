
#distribusi cms
distbusi is a content management system for the web that produces static index pages based on folders in the filesystem. It is inspired by the automatic index functions featured in several web servers. It works by traversing the file system and directory hierarchy to automatically list all the files in the directory and providing them with html classes and tags for easy styling.


##installation

distribusi depends on:
* `python-magic` 0.4+ to do automatic mime (filetype) detection
* `pillow` to generate thumbnails

using pip:
	sudo pip3 install python-magic pillow

##usage

Make a distribusi of your home folder:
	python3 distribusi -d ~/

You will find that you now have an `index.html` in every folder.

Create a quick gallery for the web:
	python3 distribusi -d /path/to/my/photos -t

This creates an `index.html` with `base64` encoded thumbnails

Generate verbose output:
	python3 distribusi -v

#✌
