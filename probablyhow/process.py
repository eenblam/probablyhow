from collections import namedtuple

import BeautifulSoup

from util import CannotCompleteRequestError

Page = namedtuple('Page', ['title', 'text'])

def process_title_response(response):
    """Just fetch the first 10, ignore pagination"""
    try:
        results = response['query']['search']
        titles = (x['title'] for x in results)
        title_string = '|'.join(titles)
    except KeyError:
        # Malformed response
        raise CannotCompleteRequestError('Cannot produce a valid title string')
    if '' == title_string:
        raise CannotCompleteRequestError('Cannot produce a valid title string')
    return title_string

def process_pageid_response(response):
    try:
        pages = response['query']['pages']
        keys = pages.keys()
    except KeyError:
        raise CannotCompleteRequestError('Cannot produce pageid list from response')
    except AttributeError:
        raise CannotCompleteRequestError('Cannot produce pageid list from response')
    for key in keys:
        yield key

def process_page_data(data):
    """Try to produce a Page from response data"""
    title = data['parse']['title']
    text = data['parse']['text']['*']
    if title and text:
        #return Page(title, text)
        return (title, text)
    return None

def process_page_stream(stream):
    """Yield only pages with the data needed to build corpus"""
    found_one = False
    for data in stream:
        try:
            page = process_page_data(data)
        except KeyError:
            continue
        if page is not None:
            found_one = True
            yield page
        if not found_one:
            raise CannotCompleteRequestError('All parsed pages invalid')

def gen_corpus_chunks(html_corpus):
    soup = BeautifulSoup.BeautifulSoup(html_corpus)
    for tag in soup.recursiveChildGenerator():
        if tag.string is not None:
            yield tag.string

def plain_corpus(html_corpus):
    return ' '.join(gen_corpus_chunks(html_corpus))


