#!/usr/bin/env python
import optparse
import os
import string

HTML_TEMPLATE_FILE="index.html.template"
ENTRY_TEMPLATE_FILE="entry.html.template"
INDEX_FILE_NAME = "index.html"

# Add option for base address to be put in head and headers specified differently from top dir
# Make attractive icons for Folders/Files
#  -- optional do mime type detection of some sort
#
# Make zipfiles of entire dir available (possibly hide under flag)
# Automate upload itself (calling this possibly as a lib)
# Make upload restartable, possibly put extra status files in hidden (.indexes) dir


def main():
	usage = """%prog dir
Generates html indexes for directory given. Indexes suitable for s3 upload."""
	parser = optparse.OptionParser(usage=usage)
	options,args = parser.parse_args()
	
	for root, dirs, files in os.walk(args[0]):
		index_file_name = os.path.join(root, INDEX_FILE_NAME)
		print "Writing", index_file_name
		index_html = createIndex(root, dirs, files)
		open(index_file_name, "w").write(index_html)
	
	return 0


# Returns html data for an index 
def createIndex(root, dirs, files):
	entry_template = string.Template(open(ENTRY_TEMPLATE_FILE).read())
	entry_string = ""
	for entry in dirs:
		mapping = {'FILELINK': entry + "/" + INDEX_FILE_NAME,'FILENAME': entry}
		entry_string += entry_template.substitute(mapping)
		
	for entry in files:
		mapping = {'FILELINK': entry, 'FILENAME': entry}
		entry_string += entry_template.substitute(mapping)
	
	html_template = string.Template(open(HTML_TEMPLATE_FILE).read())
	return html_template.substitute({
		'FILEENTRIES': entry_string,
		'DIRNAME': root
	})

if __name__ == "__main__":
	exit(main())
	