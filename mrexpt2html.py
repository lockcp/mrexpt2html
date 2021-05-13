#!/usr/bin/python3

from sys import argv
from operator import itemgetter
from jinja2 import Template

mrexpt_filename = argv[1]
html_filename = argv[1].replace('mrexpt', 'html')

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
# The first item isn't a highlight, it's some obscure metadata, so drop it
items = items[1:]

highlights = [
    {
        # No absolute location, so take the chapter number times million and add the location in the chapter
        'location': (int(item[4]) * 1000000) + int(item[6]),
        # Note is empty for highlights without a note
        'note': item[11],
        'text': item[12],
    }
    for item in items
]
# The .mrexpt is ordered by note creation, so now that we have an approximate location sort by that
highlights = sorted(highlights, key=itemgetter('location'))

# Template is copied from a Kindle APA export, no idea what Readwise expects so try not to change too much
template = Template("""
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
                              "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" >
<html xmlns="http://www.w3.org/TR/1999/REC-html-in-xml" xml:lang="en"
	lang="en">
	<head>
                <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=UTF-8" />
                <!-- HTML5 -->
                <meta charset="UTF-8"/>
		<style type="text/css">
                    .bodyContainer {
    font-family: Arial, Helvetica, sans-serif;
    text-align: center;
    padding-left: 32px;
    padding-right: 32px;
}

.notebookFor {
    font-size: 18px;
    font-weight: 700;
    text-align: center;
    color: rgb(119, 119, 119);
    margin: 24px 0px 0px;
    padding: 0px;
}

.bookTitle {
    font-size: 32px;
    font-weight: 700;
    text-align: center;
    color: #333333;
    margin-top: 22px;
    padding: 0px;
}

.authors {
    font-size: 13px;
    font-weight: 700;
    text-align: center;
    color: rgb(119, 119, 119);
    margin-top: 22px;
    margin-bottom: 24px; 
    padding: 0px;
}

.citation {
    font-size: 16px;
    font-weight: 500;
    text-align: center;
    color: #333333;
    margin-top: 22px;
    margin-bottom: 24px;
    padding: 0px;
}

.sectionHeading {
    font-size: 24px;
    font-weight: 700;
    text-align: left;
    color: #333333;
    margin-top: 24px;
    padding: 0px;
}

.noteHeading {
    font-size: 18px;
    font-weight: 700;
    text-align: left;
    color: #333333;
    margin-top: 20px;
    padding: 0px;
}

.noteText {
    font-size: 18px;
    font-weight: 500;
    text-align: left;
    color: #333333;
    margin: 2px 0px 0px;
    padding: 0px;
}

.highlight_blue {
    color: rgb(178, 205, 251);
}

.highlight_orange {
    color: #ffd7ae;
}

.highlight_pink {
    color: rgb(255, 191, 206);
}

.highlight_yellow {
    color: rgb(247, 206, 0);
}

.notebookGraphic {
    margin-top: 10px;
    text-align: left;
}

.notebookGraphic img {
    -o-box-shadow:      0px 0px 5px #888;
    -icab-box-shadow:   0px 0px 5px #888;
    -khtml-box-shadow:  0px 0px 5px #888;
    -moz-box-shadow:    0px 0px 5px #888;
    -webkit-box-shadow: 0px 0px 5px #888;
    box-shadow:         0px 0px 5px #888; 
    max-width: 100%;
    height: auto;
}

hr {
    border: 0px none;
    height: 1px;
    background: none repeat scroll 0% 0% rgb(221, 221, 221);
}

		</style>
		<script type="text/javascript">
		    
		</script>
		<title></title>
	</head>
    <body>
        <div class="bodyContainer">
            <div class="notebookFor">
Notebook for
</div>
<div class="bookTitle">
{{book_name}}
</div>
<div class="authors">
Unknown
</div>
<div class="citation">
Citation (APA): Unknown. (2021). <i>{{book_name}}</i> [Kindle Android version]. Retrieved from Amazon.com
</div>
<hr />

            <div class="sectionHeading">
Unnamed
</div>
{% for highlight in highlights %}
<div class="noteHeading">
Highlight (<span class="highlight_yellow">yellow</span>) -  Location {{highlight.location}}
</div>
<div class="noteText">
{{highlight.text}}
</div>
{% if highlight.note %}
<div class="noteHeading">
Note -  Location {{highlight.location}}
</div>
<div class="noteText">
{{highlight.note}}
</div>
{% endif %}
{% endfor %}
        </div>
    </body>
</html>
""")

with open(html_filename, 'w') as html_file:
    html_file.write(template.render(**locals()))

