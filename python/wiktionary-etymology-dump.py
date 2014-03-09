#!/usr/bin/env python2
# -*- coding: utf8 -*-

"""
wiktionary-etymology-dump: example of xml processing of wiktionary dumps
"""

# Copyright (C) 2014 martin.bukatovic@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
from optparse import OptionParser

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def get_etymology(wiki_text):
    """
    Returns etymology from mediawiki text.
    """
    result = []
    line_it = iter(wiki_text.splitlines())
    # supposing etymology is stored on a sinle line, after the heading
    for line in line_it:
        if line.startswith("===Etymology"):
            line = line_it.next().strip()
            # skipping empty lines right after the heading
            while len(line) == 0:
                line = line_it.next().strip()
            # but make sure that we are not leaving etymology section
            if line.startswith("=="):
                continue
            result.append(line)
    return result

def tag(tag_name):
    """
    Returns full etree tag name with default mediawiki namespace.
    """
    xmlns = "http://www.mediawiki.org/xml/export-0.8/"
    return "{%s}%s" % (xmlns, tag_name)

def parse_mediawiki_xml(xml_fo, dump_func):
    """
    Process mediawiki xml dump of wiktionary.
    """
    # create tag names in advance (setting default xmlns doesn't help)
    page_tag = tag("page")
    text_tag = tag("text")
    title_tag = tag("title")

    # using event based eltree parser
    itree = ET.iterparse(xml_fo, events=("start","end"))

    word_name = None
    etymology_list = None

    for event, elem in itree:
        # reset data for new word entry
        if event == "start":
            if elem.tag == page_tag:
                word_name = None
            continue
        # get data for current word entry (event == end)
        if elem.tag == title_tag:
            if not elem.text.startswith("Wiktionary:"):
                word_name = elem.text
        elif word_name is not None:
            if elem.tag == text_tag:
                etymology_list = get_etymology(elem.text)
            elif elem.tag == page_tag:
                # all data for current word entry has beed processed
                dump_func(word_name, etymology_list)

def dump_stdout(word, etymology):
    """
    Print dictionary data in a simple text format into stdout.
    """
    template = u"WORD {0}:\n{1}"
    print template.format(word, "\n".join(etymology)).encode("utf-8")

# TODO: add SQL dump method
METHODS = {
    "stdout": dump_stdout,
     }

def main(argv=None):
    """
    Read xml file from stdin or try to open first agument.
    """
    opt_parser = OptionParser(usage="usage: %prog [options] [xmlfile]")
    opt_parser.set_defaults(dump="stdout")
    opt_parser.add_option("--dump",
        action="store",
        help="dump method (def. stdout)")
    opts, args = opt_parser.parse_args()

    try:
        dump_func = METHODS[opts.dump]
    except KeyError:
        sys.stderr.write("err: unknown dump method {0}\n".format(opts.dump))
        return 1

    if len(args) == 0:
        parse_mediawiki_xml(sys.stdin, dump_func)
    else:
        with open(args[0], "r") as fobj:
            parse_mediawiki_xml(fobj, dump_func)

if __name__ == '__main__':
    sys.exit(main())
