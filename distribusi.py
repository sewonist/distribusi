#!/usr/bin/env python 
# -*- coding: iso-8859-15 -*-

#depends on python-magic 0.4
import os, magic, argparse, sys
from page_template import *

parser = argparse.ArgumentParser("""

	distribusi is a content management system for the web producing static pages based on the filesystem. It is inspired by the automatic index functions featured in several webservers. As such it uses the file system and directory hierarchy to automatically list all the files in the 
	directory and providing them with html classes and tags for easy styling.

	""")
parser.add_argument('-d', '--directory', help="Select which directory to distribute")
args = parser.parse_args()

if args.directory:
	print('Generating directory listing for', args.directory)
	directory = args.directory
else:
	directory = '.'

mime_type = magic.Magic(mime=True)

file_types = {'image':'<img class="image" src="{}"></img>', 'pdf':'<a href="{}" class="pdf">{}</a>', 
'text':'<a href="{}" class="text">{}</a>', 'video':'<video class="video" src="{}"></video>', 'audio':'<audio controls class="audio"> <source src="{}"></source></audio>','html':'<a href="{}">{}</a>'}

def dict_by_value(dictionary, value):
	return(list(dictionary.keys())[list(dictionary.values()).index(value)]) # returns the key for the given value
def div(mime, tag, *values):
	#name, full_path
	if 'image' in mime:
		html ='<div class="{}">'.format(values[0])+tag+'</br><span class="filename">{}</span></div>'.format(values[0])
	else:
		html = '<div class="{}">'.format(values[0])+tag+'</div>'.format(values[0])
	return html

for root, dirs, files in os.walk(directory):
	html = []
	for name in files:
		if 'index.html' not in name:
			full_path = os.path.join(root,name)
			mime = mime_type.from_file(full_path)
			mime, format = mime.split('/') #example: text plain

			if mime in file_types:
				if name.endswith('.html'):
					a = open(full_path).read()
				else:
					a = file_types[mime]

			if format in file_types:
					a = file_types[format]

			if mime not in file_types and format not in file_types: #to catch exceptions we haven't defined in file_types before
				a = "<a href='{}'>{}</a>"
				# print (mime,format, name)

			a = a.replace('{}',name)
			html.append(div(mime,a,name))
			#html.append(a)
	if root != directory:
		html.append('<a href="../">../</a>')

	for name in dirs:
		i = os.path.join(root,name)
		a = "<a href='{}' class='dir'>{}/</a>".replace('{}',name)
		# print(a)
		html.append(div('dir',a,'folder'))


	with open(os.path.join(root,'index.html'),'w') as f:
		f.write(html_head)
		for line in html:
			f.write(line+'\n')
		f.write(html_footer)