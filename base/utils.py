""" Small methods for generic use """

# standard library
import itertools
import urlparse


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.izip_longest(
        *args
    ))


def extract_youtube_id(url):
        """
        Extracts the youtube id from a youtube url, it supports several
        formats.

        Based on
        http://stackoverflow.com/a/7936523/982915

        """
        if not url:
            return ''

        query = urlparse.urlparse(url)
        if query.hostname == 'youtu.be':
            return query.path[1:]
        elif query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch':
                p = urlparse.parse_qs(query.query)
                return p['v'][0]
            if query.path[:7] == '/embed/':
                return query.path.split('/')[2]
            if query.path[:3] == '/v/':
                return query.path.split('/')[2]
        else:
            return ''
