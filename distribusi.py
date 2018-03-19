#!/usr/bin/env python3 
# -*- coding: iso-8859-15 -*-

#depends on python-magic 0.4
import os, magic, argparse, sys, base64
from page_template import *
from PIL import Image 
from io import BytesIO

parser = argparse.ArgumentParser("""
distbusi is a content management system for the web that produces static index pages based on folders in the filesystem. It is inspired by the automatic index functions featured in several web servers. It works by traversing the file system and directory hierarchy to automatically list all the files in the directory and providing them with html classes and tags for easy styling.
""")
parser.add_argument('-d', '--directory', help="Select which directory to distribute")
parser.add_argument('-v', '--verbose', help="Print verbose debug output", action="store_true")
parser.add_argument('-t', '--thumbnail', help="Generate 150x150 thumbnails for images", action="store_true")
parser.add_argument('-n', '--no-template', help="Don't use the template to ouput html",action="store_true")

#Todo:
# build an 'undo' function that traverses the same directories and removes the index.html files
# set the 'maxdepth'
# toggle .folders
# find better way for template handling?


args = parser.parse_args()

if args.directory:
	if args.verbose:
		print('Generating directory listing for', args.directory)
	if args.thumbnail:
		print('Making thumbnails')
	directory = args.directory
else:
	directory = '.'

mime_type = magic.Magic(mime=True)

file_types = {'image':'<img class="image" src="{}">', 'pdf':'<object data="{}" class="pdf" type="application/pdf"><embed src="{}" type="application/pdf" /></object>', 
'text':'<a href="{}" class="text">{}</a>', 'video':'<video class="video" controls><source src="{}"></source></video>', 'audio':'<audio controls class="audio"> <source src="{}"></source></audio>'}

code_types = ['x-c', 'html']

def thumbnail(image, name):
	size = 450,450
	im = Image.open(image)
	im.thumbnail(size)
	output = BytesIO()
	im.save(output, format='JPEG')
	im_data = output.getvalue()
	data_url = base64.b64encode(im_data).decode()
	return "<a href='{}'><img class='thumbnail' src='data:image/jpg;base64,{}'></a>".format(name, data_url)

def div(mime, tag, *values):
	#name, full_path
	id_name = values[0].split('.')[0].replace(' ', '_')
	if 'image' in mime:
		html = '<div id="{}">'.format(id_name)+tag+'<br><span class="filename">{}</span></div>'.format(values[0]) 
	elif 'pdf' in format:
		html ='<div id="{}">'.format(id_name)+tag+'<br><class="filename">{}</span></div>'.format(values[0])
	else:
		html = '<div id="{}">'.format(id_name)+tag+'</div>'.format(values[0])
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

				if mime == 'image' and args.thumbnail:
					a = thumbnail(full_path, name)
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
		if not args.no_template:
			f.write(html_head)
		for line in html:
			f.write(line+'\n')
		if not args.no_template:
			f.write(html_footer)
