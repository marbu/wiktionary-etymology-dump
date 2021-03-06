# Wiktionary Etymology Dump

The goal of these scripts is to to extract etymology data from wiktionary
mediawiki xml dump. The code is not a polished tool, it's rather just
a demonstration of several different approaches.

Different approaches tried here:

 * `stx-xsl-awk`: stx (or xslt for comparison) template with awk script
 * `python-iterparse`: python script using `xml.etree.ElementTree` (doesn't work)
 * `python-sax`: python script using `xml.sax` module

## Requirements

The input file is a mediawiki xml dump of english wiktionary which is quite
large (it takes 400 MB as compressed bzip file). So it makes sense to use
streaming processing - otherwise we would have to load the whole parse xml tree
into memory which is insane :)

### Input XML file

You can get the wiktionary xml dump here:
[enwiktionary-latest-pages-articles.xml.bz2](http://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-pages-articles.xml.bz2)

Then for each `/mediawiki/page` in the file, we are interested in:

 * `/mediawiki/page/title/text()`, eg `woordenboek`
 * `/mediawiki/page/revision/text/text()`, but only the etymology section, eg:

```
===Etymology===
{{compound|woord|boek|t1=word|t2=book|lang=nl}}. Akin to German {{term|Wörterbuch|lang=de}} and West Frisian {{term|wurdboek|lang=fy}}.
```

The problem here is that a single word may contain multiple etymology entries
(even zero), so we need to check for additional etymology headings in the text.
Fortunately mediawiki syntax is quite simple, so no need to use special parse
for this task.

### Output

Simple text output (for check and debugging), with a possibility to change it
to sql input statements.

## Notes

For real work, please refer to
[mediawiki xml tools](https://meta.wikimedia.org/wiki/Data_dumps/Tools_for_importing)
