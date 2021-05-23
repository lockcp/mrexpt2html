#!/usr/bin/python3

import argparse
from datetime import datetime
from operator import itemgetter

import jinja2
from titlecase import titlecase

DATETIMESTR = ''.join([ch for ch in datetime.utcnow().isoformat()[0:19] if ch.isdigit()])

def capitalize_title(ugly_title):
    if (all(ch.isupper() or not(ch.isalpha()) for ch in ugly_title) or
        all(ch.islower() or not(ch.isalpha()) for ch in ugly_title)):
        # Title is ugly, titlecase it
        return titlecase(ugly_title)
    else:
        return ugly_title

def capitalize_headings(highlights):
    for highlight in highlights:
        if highlight['note'] and highlight['note'].startswith('.h'):
            highlight['text'] = capitalize_title(highlight['text'])

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

def do_convert(mrexpt_filename, html_filename, debug=True, titlecap=True,
               book_name=None, author='Unknown'):
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

    if book_name is None:
        # The book name and filename is present in every highlight, so pick it up from the first
        book_name = items[1][1] or items[1][2]
        if debug:
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
    if titlecap:
        capitalize_headings(highlights)

    render_vars = {
        'book_name': book_name,
        'author': author,
        'highlights': highlights,
        'year': DATETIMESTR[:4],
    }
    with open(html_filename, 'w') as html_file:
        html_file.write(load_template().render(render_vars))

def boolstr(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 'on', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'off', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="input file")
    parser.add_argument("-d", "--debug", type=boolstr, default=True,
                        help="run in debug mode - unique file and book name")
    parser.add_argument("-t", "--titlecap", type=boolstr, default=True,
                        help="convert ALL CAPS headings to Title Cap")
    parser.add_argument("-b", "--book", type=str,
                        help="book name (override the one specified in the .mrexpt file)",
                        default=None)
    parser.add_argument("-a", "--author", type=str,
                        help="name of the author(s)",
                        default='Unknown')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    mrexpt_filename = args.input
    html_filename = mrexpt_filename.replace('mrexpt', 'html')
    if args.debug:
        html_filename = html_filename.replace('.html', '-' + DATETIMESTR + '.html')

    do_convert(mrexpt_filename, html_filename, debug=args.debug, titlecap=args.titlecap,
               book_name=args.book, author=args.author)