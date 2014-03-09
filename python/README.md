# Python Mediawiki Import

So far, the initial version using `ElementTree.iterparse()` doesn't work for me:

```
$ time bzcat enwiktionary-latest-pages-articles.xml.bz2 | ./wiktionary-etymology-dump.py > /dev/null
Traceback (most recent call last):
  File "./wiktionary-etymology-dump.py", line 130, in <module>
    sys.exit(main())
  File "./wiktionary-etymology-dump.py", line 124, in main
    parse_mediawiki_xml(sys.stdin, dump_func)
  File "./wiktionary-etymology-dump.py", line 77, in parse_mediawiki_xml
    for event, elem in itree:
  File "<string>", line 100, in next
MemoryError

real    38m28.564s
user    4m40.179s
sys     0m16.592s
```
