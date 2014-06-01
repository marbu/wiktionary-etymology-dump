#!/bin/bash
XML_INPUT=../example.xml
joost.sh $XML_INPUT mediawiki-xml2text.stx | awk -f extract-etymology.awk
