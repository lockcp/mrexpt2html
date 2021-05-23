# mrexpt2html

**Convert Moon+ Reader highlight export to Readwise-compatible HTML**

This utility makes it ~~easy~~ possible to upload highlights from [Moon+ Reader](https://play.google.com/store/apps/details?id=com.flyersoft.moonreaderp&hl=en&gl=US) to [Readwise](https://readwise.io/).

## Installation
Clone this repository and install the python packages `jinja2` and `titlecase`.

## Usage
1. Export your highlights from Moon+ Reader by opening the highlights tab, clicking the share icon and choosing export to file from the menu.
2. This will generate a .mrexpt file. Save it and upload it to where you can run this script (for exmaple by emailing it to yourself or uploading to GDrive or Dropbox).
3. Run this script, specifying the .mrexpt as the input file. For example:
`./mrexpt2html my-book-highlights.mrexpt`
4. An HTML file will be generated. Send it to add@readwise.io and it will be imported (wait for an email back from Readwise letting you know that the import was successful ... or not).
5. Book name and author aren't captured, so edit metadata from within Readwise.

### Options
**`debug`**
Turned on by default, and ensures that the book and file name are unique (by adding a timestamp). That makes it easy to repeatedly import the same book to Readwise without collision - each import will be considered a different book. That's convenient for debugging this script, but if you do want to upload the same book over and over again, turn this off like this:

`./mrexpt2html --debug=false my-book-highlights.mrexpt`


**`titlecap`**
Turned on by default and converts chapter headings (highlights with notes like .h1/.h2/.h3) to *Title Cap* if they are *ALL CAPITAL* or *all lowercase*. This isn't specific to either Moon+ Reader or Readwise, but it's nice to be able to make this change - many books use ugly allcaps for chapter headings for typographical reasons but outside of the book formatting they're just not that nice. You can turn this off like this:

`./mrexpt2html --titlecap=false my-book-highlights.mrexpt`


**`book`**
Override the book name. Use the value specified instead of the book name available in the .mrexpt file.


**`author`**
Specify the author(s) which isn't available in the .mrexpt file. If unspecified the author is written as 'Unknown'.

---

Enjoy, let me know if there are any issues or suggestions by filing issues, and of course pull requests are very welcome. The code is public domain so you can do with it whatever you want.