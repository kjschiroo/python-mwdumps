import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime


ENDPOINT_URL = "https://dumps.wikimedia.org"


class Error(Exception):
    pass


class WikiConnectionError(Error):
    pass


class DumpCompletionStateUncertainError(Error):
    pass


class NoCompleteDumpsError(Error):
    pass


def _get_html(url):
    r = requests.get(url)
    if r.status_code != 200:
        raise WikiConnectionError(url)
    return r.text


def get_dump_dates_for(wiki):
    result = []
    html = _get_html('/'.join([ENDPOINT_URL, wiki]))
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        match = re.match(r'(\d{8})', link.text)
        if match is not None:
            result.append(datetime.strptime(match.group(1), '%Y%m%d'))
    return result


def get_dump_page_html(wiki, date):
    date_str = date.strftime('%Y%m%d')
    return _get_html("/".join([ENDPOINT_URL, wiki, date_str]))


def is_dump_complete(wiki, date):
    html = get_dump_page_html(wiki, date)
    soup = BeautifulSoup(html, 'html.parser')
    if len(soup.findAll("span", {"class": "in-progress"})) == 1:
        return False
    if len(soup.findAll("span", {"class": "done"})) == 1:
        return True
    raise DumpCompletionStateUncertainError()


def most_recent_completed_dump_date_for(wiki):
    available_dump_dates = get_dump_dates_for(wiki)
    while len(available_dump_dates) > 0:
        recent = max(available_dump_dates)
        if is_dump_complete(wiki, recent):
            return recent
        else:
            available_dump_dates.remove(recent)
    raise NoCompleteDumpsError()


def has_dump_on_date(wiki, date):
    available_dump_dates = get_dump_dates_for(wiki)
    return date in available_dump_dates


def get_dump_file_urls(wiki, date=None, matching=['.*']):
    if date is None:
        date = most_recent_completed_dump_date_for(wiki)
    elif not has_dump_on_date(wiki, date):
        raise NoCompleteDumpsError()
    return _get_dump_file_urls_matching(wiki, date, matching)


def _get_dump_file_urls_matching(wiki, date, regex_list):
    matching_file_urls = {}
    file_url_map = _get_dump_filesnames_and_urls_for(wiki, date)
    for filename, url in file_url_map.items():
        matching_regex = [r for r in regex_list if re.search(r, filename)]
        if len(matching_regex) > 0:
            matching_file_urls[filename] = url
    return matching_file_urls


def _get_file_url(wiki, date, filename):
    date_str = date.strftime('%Y%m%d')
    return '/'.join([ENDPOINT_URL, wiki, date_str, filename])


def _get_sha1sums(wiki, date):
    sha_map = {}
    date_str = date.strftime('%Y%m%d')
    sha1_file = '{0}-{1}-sha1sums.txt'.format(wiki, date_str)
    url = _get_file_url(wiki, date, sha1_file)
    content = _get_html(url)
    for line in content.strip().split('\n'):
        sha1, filename = line.split()
        sha_map[filename] = sha1
    return sha_map


def _get_dump_filesnames_and_urls_for(wiki, date):
    sha_map = _get_sha1sums(wiki, date)
    return dict([(filename, _get_file_url(wiki, date, filename))
                 for filename in sha_map])
