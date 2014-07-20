#!/usr/bin/env python2
# -*- coding: utf8 -*-

"""
wiktionary-etymology-dump: extracts etymology from wiktionary xml dump
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


from optparse import OptionParser
import sys
import xml.sax
import re


def get_etymology(content):
    """
    Filter etymology from content of /mediawiki/page/revision/text element.

    @param content: character content of the text element
    @type  content: list
    """
    result = []
    # check for empty input
    if content is None or len(content) == 0:
        return result
    # supposing etymology is stored on a sinle line, after the heading
    line_it = iter(content)
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


class WiktionaryHandler(xml.sax.ContentHandler):
    """
    Wiktionary etymology extracting SAX handler.
    """

    ignore_title_re = re.compile("^[A-Z][a-zA-Z]+:")

    def __init__(self, dump_func):
        xml.sax.ContentHandler.__init__(self)
        self._dump_func = dump_func
        self._in_vpage = False  # inside page element of vocabulary page
        self._in_title = False
        self._in_text = False
        self._word = None
        self._content_list = []

    def startElement(self, name, attrs):
        if name == "page":
            self._in_vpage = True
        elif name == "title":
            self._in_title = True
        elif name == "text":
            self._in_text = True

    def endElement(self, name):
        if name == "page":
            if self._in_vpage == True:
                self._dump_func(self._word, get_etymology(self._content_list))
            self._in_vpage = False
        elif name == "title":
            self._in_title = False
        elif name == "text":
            self._in_text = False

    def characters(self, content):
        if not self._in_vpage:
            return
        if self._in_title:
            if self.ignore_title_re.match(content):
                self._in_vpage = False
            else:
                self._word = content
                self._content_list = []
        elif self._in_text:
            self._content_list.append(content)

def parse_wiktionary_xml(xml_file, dump_func):
    """
    Run etymology filtering of Wiktionary XML dump.
    """
    parser = xml.sax.make_parser()
    parser.setContentHandler(WiktionaryHandler(dump_func))
    parser.parse(xml_file)

def dump_text(word, etymology):
    """
    Print dictionary data in a simple text format into stdout.
    """
    template = u"WORD {0}\n{1}"
    print template.format(word, "\n".join(etymology)).encode("utf-8")

METHODS = {
    "text": dump_text,
     }

def main(argv=None):
    """
    Read xml file from stdin or try to open file passed as first agument.
    """
    opt_parser = OptionParser(usage="usage: %prog [options] [xmlfile]")
    opt_parser.set_defaults(dump="text")
    opt_parser.add_option("--dump",
        action="store",
        help="dump method (simple text format is the default)")
    opts, args = opt_parser.parse_args()

    try:
        dump_func = METHODS[opts.dump]
    except KeyError:
        sys.stderr.write("err: unknown dump method {0}\n".format(opts.dump))
        return 1

    if len(args) == 0:
        parse_wiktionary_xml(sys.stdin, dump_func)
    else:
        with open(args[0], "r") as fobj:
            parse_wiktionary_xml(fobj, dump_func)

if __name__ == '__main__':
    sys.exit(main())
