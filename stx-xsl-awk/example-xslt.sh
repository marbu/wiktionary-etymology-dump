#!/bin/bash
XML_INPUT=../example.xml
xsltproc mediawiki-xml2text.xsl $XML_INPUT | awk -f extract-etymology.awk
