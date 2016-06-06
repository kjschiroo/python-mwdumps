"""cmdline

Usage:
    cmdline --wiki=<wiki_name> [--date=<date>]
        [--config=<config_file>] [--verbose] <output_path>
    cmdline (-h | --help)
Options:
    --config=<config_file>       Configuration file containing a set of regexes,
                                    one per line, that matches dump files to be
                                    downloaded.
    --wiki=<wiki_name>           Abbreviation for wiki of interest
    --date=<date>                Get dump on <date>. Defaults to most recent.
    -v, --verbose                    Generate verbose output
"""
from docopt import docopt
import dumps
import downloader
from dateutil import parser
import os.path
import os
import logging


def _parse_config_file(filepath):
    with open(filepath) as f:
        return [line.strip() for line in f]


def _download_matching_dump_files(wiki, date, regexes, output_path):
    date_str = date.strftime('%Y%m%d')
    full_path_url_map = {}
    full_output_dir = os.path.join(output_path, wiki, date_str)
    if not os.path.exists(full_output_dir):
        os.makedirs(full_output_dir)
    file_url_map = dumps.get_dump_file_urls(wiki, date, regexes)
    for filename, url in file_url_map.items():
        full_path_url_map[os.path.join(full_output_dir, filename)] = url
    downloader.download_files_in_map(full_path_url_map)


def main(args):
    if args['--verbose']:
        logging.basicConfig(level=logging.INFO)
    date = None
    if args['--date'] is not None:
        date = parser.parse(args['--date'])
    else:
        date = dumps.most_recent_completed_dump_date_for(args['--wiki'])
    regexes = ['.*']
    if args['--config'] is not None:
        regexes = _parse_config_file(args['--config'])
    _download_matching_dump_files(args['--wiki'],
                                  date,
                                  regexes,
                                  args['<output_path>'])


if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(arguments)
