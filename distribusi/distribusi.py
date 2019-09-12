import base64
import os
import subprocess
from io import BytesIO

import magic
from PIL import Image

from distribusi.page_template import html_footer, html_head
from distribusi.mappings import CODE_TYPES, FILE_TYPES, SUB_TYPES

MIME_TYPE = magic.Magic(mime=True)


def caption(image):
    try:
        process = subprocess.Popen(['exiftool', '-Comment', image], stdout=subprocess.PIPE)
        out, err = process.communicate()
    except Exception as e:
        print(e)
        print('Do you have exiftool installed?')
    try:
        caption = out.decode("utf-8").split(": ", 1)[1]
    except:
        caption = ''
    return caption


def thumbnail(image, name, args):
    try:
        size = (450, 450)
        im = Image.open(image)
        im.thumbnail(size)
        output = BytesIO()
        im.save(output, format='JPEG')
        im_data = output.getvalue()
        data_url = base64.b64encode(im_data).decode()
        if args.captions:
            cap = caption(image)
        else:
            cap = name
        return (
            "<figure><a href='{}'><img class='thumbnail' src='data:image/jpg;base64,{}'></a><figcaption>{}</figcaption></figure>"
        ).format(name, data_url, cap)
    except Exception as e:
        print('Thumbnailer:',e)
        return  "<figure><a href='{}'><img src='{}'></a><figcaption>{}</figcaption></figure>".format(name, name,name)
        


def div(args, type_, subtype, tag, name):
    id_name = name.split('.')[0].replace(' ', '_')
    if args.no_filenames:
        filename = ''
    else:
        filename = '<span class="filename">{}</span>'.format(name)

    if 'image' in type_:
        html = '<div id="{}" class="{}">{}</div>'
    elif 'pdf' in subtype:
        html = '<div id="{}" class="{}">{}' + filename + '</div>'
    elif 'dir' in type_ or 'html' in subtype or 'unkown-file' in subtype:
        html = '<div id="{}" class="{}">{}</div>'
    else:
        html = '<div id="{}" class="{}">{}' + filename +'</div>'

    return html.format(id_name, subtype, tag)


def distribusify(args, directory):  # noqa
    for root, dirs, files in os.walk(directory):
        if not args.remove_index:
            html = []
              
            if args.verbose:
                print('Generating directory listing for', root)

            for name in files:
                if 'index.html' not in name:
                    full_path = os.path.join(root, name)
                    mime = MIME_TYPE.from_file(full_path)
                    # example: MIME plain/text becomes 'type' plain 'subtype' text
                    type_, subtype = mime.split('/')  

                    if args.verbose:
                        print('Found', name,'as', mime)

                    if type_ in FILE_TYPES:
                        # expansion for different kind of textfiles
                        if type_ == 'text':
                            if name.endswith('.html') or subtype == 'html':
                                subtype = 'html'
                                # what types of text files to expand
                                a = '<section id="{}">{}</section>'.format(name, open(full_path).read())
                            elif subtype in CODE_TYPES or name.endswith('.txt'):
                                # if the plain text is code,
                                # which types do we wrap in pre-tags?
                                a = "<pre>" + open(full_path).read() + "</pre>"
                            else:
                                subtype = subtype+' unkown-file'
                                a = "<a href='{}'>{}</a>"
                                #a = FILE_TYPES[type_]

                        if type_ == 'image':
                            caption = name
                            if args.thumbnail:
                                a = thumbnail(full_path, name, args)
                            if args.no_filenames:
                                caption = ""
                            if args.captions:
                                caption = caption(full_path)

                            a = FILE_TYPES[type_].format(name, caption)

                    if subtype in SUB_TYPES:
                        a = SUB_TYPES[subtype]

                    if type_ not in FILE_TYPES and subtype not in SUB_TYPES:
                        # catch exceptions not yet defined in FILE_TYPES or SUB_TYPES
                        a = "<a href='{}'>{}</a>"
                        if args.verbose:
                            message = 'not in list of file types, adding as plain href: \n'
                            print(type_, subtype, message, name)
                            type_ ='unkown-file'
                    a = a.replace('{}', name)
                    html.append(div(args, type_, subtype, a, name))

            if root != directory:
                html.append('<a href="../">../</a>')

            for name in dirs:
                a = "<a href='{}'>{}/</a>".replace('{}', name)
                html.append(div(args,'dir', 'dir', a, 'folder'))

            with open(os.path.join(root, 'index.html'), 'w') as f:
                if not args.no_template:
                    if args.style:
                        fs = open(args.style, "r")
                        style = fs.read()
                        styled_html_head = html_head % style
                    else:
                        styled_html_head = html_head % ''
                    f.write(styled_html_head)

                for line in html:
                    f.write(line + '\n')

                if not args.no_template:
                    f.write(html_footer)
        if args.remove_index:
            index = os.path.join(root, 'index.html')
            if 'index.html' in files:
                if args.verbose:
                    print('Removing index.html from', root)
                try:
                    os.remove(index)
                except Exception as e:
                    print(e)
