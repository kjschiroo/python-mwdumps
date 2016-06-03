import urllib
import logging


def download_files_in_map(filemap):
    opener = urllib.request.URLopener()
    for path, url in filemap.items():
        logging.info('{0} <-- {1}'.format(path, url))
        opener.retrieve(url, path)
