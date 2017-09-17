# mwdumps #

## install ##
```
git clone https://github.com/kjschiroo/python-mwdumps.git
cd python-mwdumps
python3 setup.py install
```

## usage ##
```
> python3 -m mwdumps.cmdline
Usage:
    mwdumps --wiki=<wiki_name> [--date=<date>] [--threads=<threads>]
        [--config=<config_file>] [--verbose] <output_path>
    mwdumps (-h | --help)
Options:
    --config=<config_file>       Configuration file containing a set of regexes,
                                    one per line, that matches dump files to be
                                    downloaded.
    --wiki=<wiki_name>           Abbreviation for wiki of interest.
    --date=<date>                Get dump on <date>. Defaults to most recent.
    --threads=<threads>          Number of parallel downloads [default: 3].
    -v, --verbose                Generate verbose output.
```

## config_file ##
The configuration file should contain a set of regexes that match the
filenames. If it is omitted then we __assume that all of the available files
in the dump should be downloaded.__

### Examples ###
English Wikipedia revision metatdata, no page text:  
`enwiki-\d+-stub-meta-history\d+\.xml.gz`

Wikidata, all pages, current version only.  
`wikidatawiki-\d+-pages-meta-current\d+\.xml-p\d+p\d+.bz2`
