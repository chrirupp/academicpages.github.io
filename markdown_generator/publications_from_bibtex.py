import pybtex.database
from pybtex.database import BibliographyData
import os

bib_data = pybtex.database.parse_file('publications.bib')

# YAML is very picky about how it takes a valid string,
# so we are replacing single and double quotes (and ampersands)
# with their HTML encoded equivalents. This makes them look not
# so readable in raw format, but they are parsed and rendered nicely.

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;"
    }


def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)


# ## Creating the markdown files
# 
# This is where the heavy lifting is done.
# This loops through all the publications,
# then starts to concatentate a big string (```md```)
# that contains the markdown for each type. It does the
# YAML metadata first, then does the description for the
# individual page. If you don't want something to appear
# (like the "Recommended citation")

for key, bib_item in bib_data.entries.items():
    print(key)
    fields = bib_item.fields
    md_filename = fields['year'] + '-' + key + ".md"
    html_filename = fields['year'] + '-' + key

    if 'booktitle' in fields:
        venue_str = html_escape(fields['booktitle'])
    elif 'journal' in fields:
        venue_str = html_escape(fields['journal'])
    else:
        print('Could not find venue for ' + key + '!')

    if 'url' in fields:
        url_str = fields['url']
        bib_item.fields._dict.pop('url')  # hack because their dict does not support del
        bib_item.fields.order.remove('url')  # remove url to not have it in the displayed bibtex
    else:
        url_str = None
    citation = BibliographyData(entries={key: bib_item})
    citation_str = citation.to_string("bibtex")
    citation_str = citation_str.encode("unicode_escape").decode("utf-8")
    citation_str = citation_str.translate(str.maketrans({'"':  "\\\""}))
    
    authors = ' and '.join([str(c) for c in bib_item.persons['author']])
    
    ## YAML variables
    
    md = "---\ntitle: \"" + html_escape(fields['title']) + '"\n'
    md += """collection: publications"""
    md += """\npermalink: /publication/""" + html_filename
    md += "\nyear: " + fields['year']
    md += "\nvenue: '" + venue_str + "'"
    md += "\nauthors: '" + html_escape(authors) + "'"
    
    if url_str:
        md += "\npaperurl: '" + url_str + "'"

    md += "\nbibtex: \"" + citation_str + "\""
    md += "\n---"

    md_filename = os.path.basename(md_filename)
    with open("../_publications/" + md_filename, 'w') as f:
        f.write(md)


