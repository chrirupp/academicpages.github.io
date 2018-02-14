from pybtex.database.input import bibtex
from pybtex.database import BibliographyData
import os

parser = bibtex.Parser()
bib_data = parser.parse_file('publications.bib')
print(bib_data.entries.keys())

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
    fields = bib_item.fields
    md_filename = fields['year'] + '-' + key + ".md"
    html_filename = fields['year'] + '-' + key
    citation = BibliographyData(entries={key: bib_item})
    citation_str = citation.to_string("bibtex")
    citation_str = citation_str.encode("unicode_escape").decode("utf-8")
    citation_str = citation_str.translate(str.maketrans({'"':  "\\\""}))
    
    ## YAML variables
    
    md = "---\ntitle: \"" + html_escape(fields['title']) + '"\n'
    md += """collection: publications"""
    md += """\npermalink: /publication/""" + html_filename
    md += "\nyear: " + fields['year']
    md += "\nvenue: '" + html_escape(fields['booktitle']) + "'"
    
    if 'url' in fields:
        md += "\npaperurl: '" + fields['url'] + "'"

    md += "\nbibtex: \"" + citation_str + "\""
    md += "\n---"

    md_filename = os.path.basename(md_filename)
    with open("../_publications/" + md_filename, 'w') as f:
        f.write(md)


