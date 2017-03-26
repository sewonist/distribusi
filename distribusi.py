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
parser.add_argument('-v', '--verbose', help="Print verbose debug output", action="store_true")
args = parser.parse_args()

if args.directory:
	print('Generating directory listing for', args.directory)
	directory = args.directory
else:
	directory = '.'

mime_type = magic.Magic(mime=True)

file_types = {'image':'<img class="image" src="{}"></img>', 'pdf':'<object data="{}" class="pdf" type="application/pdf"><embed src="{}" type="application/pdf" /></object>', 
'text':'<a href="{}" class="text">{}</a>', 'video':'<video class="video" controls><source src="{}"></source></video>', 'audio':'<audio controls class="audio"> <source src="{}"></source></audio>','html':'<a href="{}">{}</a>'}

code_types = ['x-c', 'html']


def dict_by_value(dictionary, value):
	return(list(dictionary.keys())[list(dictionary.values()).index(value)]) # returns the key for the given value
def div(mime, tag, *values):
	#name, full_path
	class_name = values[0].split('.')[0].replace(' ', '_')
	if 'image' in mime:
		html ='<div class="{}">'.format(class_name)+tag+'</br><span class="filename">{}</span></div>'.format(values[0])

	elif 'pdf' in format:
		html ='<div class="{}">'.format(class_name)+tag+'</br><class="filename">{}</span></div>'.format(values[0])
	else:
		html = '<div class="{}">'.format(class_name)+tag+'</div>'.format(values[0])
	return html

for root, dirs, files in os.walk(directory):
	html = []
	if args.verbose:
		print ('Listing', root)
	for name in files:
		if args.verbose:
			print ('Adding', name)
		if 'index.html' not in name:
			full_path = os.path.join(root,name)
			mime = mime_type.from_file(full_path)
			mime, format = mime.split('/') #example: text plain

			if args.verbose:
				print(mime, format)

			if mime in file_types: #expansion for different kind of textfiles
				if mime == 'text':
					if name.endswith('.html') or name.endswith('.txt'): #what types of text files to expand
						a = open(full_path).read()
					elif format in code_types: #if the plain text is code, which types do we wrap in pre-tags?
						a = "<pre>"+open(full_path).read()+"</pre>"
					else:
						a = file_types[mime]
				else:
					a = file_types[mime]

			if format in file_types:
					a = file_types[format]

			if mime not in file_types and format not in file_types: #to catch exceptions we haven't defined in file_types before
				a = "<a href='{}'>{}</a>"
				if args.verbose:
					print ('mime-type not in list, adding as href: \n', mime,format, name)

			a = a.replace('{}',name)
			html.append(div(mime,a,name))
			#html.append(a)
	if root != directory:
		html.append('<a href="../">../</a>')

	for name in dirs:
		i = os.path.join(root,name)
		a = "<a href='{}' class='dir'>{}/</a>".replace('{}',name)
		html.append(div('dir',a,'folder'))


	with open(os.path.join(root,'index.html'),'w') as f:
		f.write(html_head)
		for line in html:
			f.write(line+'\n')
		f.write(html_footer)