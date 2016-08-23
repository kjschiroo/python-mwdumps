import urllib
import logging
from queue import Queue
from asyncio import QueueEmpty
from threading import Thread
# from multiprocessing.pool import ThreadPool


def download_files_in_map(filemap, threads=1):
    q = Queue()
    for i in filemap.items():
        q.put(i)
    for i in range(threads):
        t = Thread(target=_thread_download, args=(q,), daemon=True)
        t.start()
    q.join()


def _thread_download(q):
    opener = urllib.request.URLopener()
    while not q.empty():
        try:
            item = q.get_nowait()
        except QueueEmpty as e:
            continue
        path, url = item
        logging.info('{0} <-- {1}'.format(path, url))
        opener.retrieve(url, path)
        q.task_done()


# def download_files_in_map(filemap, threads=1):
#     with ThreadPool(threads) as pool:
#         pool.map(_thread_download_star, filemap.items())
#
#
# def _thread_download_star(args):
#     _thread_download(*args)
#
#
# def _thread_download(path, url):
#     logging.info('{0} <-- {1}'.format(path, url))
#     opener = urllib.request.URLopener()
#     opener.retrieve(url, path)
