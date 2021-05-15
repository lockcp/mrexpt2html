#!/usr/bin/python3

from sys import argv
from operator import itemgetter
from datetime import datetime

import jinja2


DEBUG = True
DATETIMESTR = ''.join([ch for ch in datetime.utcnow().isoformat()[0:19] if ch.isdigit()])

mrexpt_filename = argv[1]
html_filename = argv[1].replace('mrexpt', 'html')
if DEBUG:
    html_filename = html_filename.replace('.html', '-' + DATETIMESTR + '.html')

def load_template():
    return jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="./")).get_template("readwise.j2")

def fix_highlight_text(unfixed):
    return unfixed.replace('<BR>', '\n')

def remove_duplicate_highlights(full_highlights):
    unique_highlights = []
    for full_highlight in full_highlights:
        if len(unique_highlights) > 0:
            if (unique_highlights[-1]['text'] == full_highlight['text'] and
                unique_highlights[-1]['note'] == full_highlight['note']):
                continue
        unique_highlights.append(full_highlight)
    return unique_highlights

items = []

with open(mrexpt_filename, 'r') as mrexpt_file:
    lines = mrexpt_file.read().splitlines()
    current_item = []
    for line in lines:
        # A line with `#` starts a new item
        if line == '#':
            items.append(current_item)
            current_item = []
        else:
            # Each line is a field
            current_item.append(line)
    items.append(current_item)

# The book name and filename is present in every highlight, so pick it up from the first
book_name = items[1][1] or items[1][2]
if DEBUG:
    book_name = book_name + ' - ' + DATETIMESTR
# The first item isn't a highlight, it's some obscure metadata, so drop it
items = items[1:]

highlights = [
    {
        # No absolute location, so take the chapter number times million and add the location in the chapter
        'location': (int(item[4]) * 1000000) + int(item[6]),
        # Note is empty for highlights without a note
        'note': item[11],
        'text': fix_highlight_text(item[12]),
    }
    for item in items
]
# The .mrexpt is ordered by note creation, so now that we have an approximate location sort by that
highlights = remove_duplicate_highlights(sorted(highlights, key=itemgetter('location')))

with open(html_filename, 'w') as html_file:
    html_file.write(load_template().render(**locals()))
