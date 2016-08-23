import urllib
import logging
from multiprocessing.pool import ThreadPool


def download_files_in_map(filemap, threads=1):
    with ThreadPool(threads) as pool:
        pool.map(_thread_download_star, filemap.items())


def _thread_download_star(args):
    _thread_download(*args)


def _thread_download(path, url):
    logging.info('{0} <-- {1}'.format(path, url))
    opener = urllib.request.URLopener()
    opener.retrieve(url, path)
