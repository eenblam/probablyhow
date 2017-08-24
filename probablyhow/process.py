from collections import namedtuple

import BeautifulSoup

Page = namedtuple('Page', ['title', 'text'])

def process_title_response(response):
    """Just fetch the first 10, ignore pagination"""
    try:
        results = response['query']['search']
    except KeyError:
        #TODO Malformed response
        return ''
    titles = (x['title'] for x in results)
    return '|'.join(titles)

def process_pageid_response(response):
    try:
        pages = response['query']['pages']
    except KeyError:
        #TODO Malformed response - JSON cannot be parsed
        return
    try:
        keys = pages.keys()
    except AttributeError:
        #TODO Malformed response - JSON parsed, but to wrong type
        return
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
    for data in stream:
        try:
            page = process_page_data(data)
        except KeyError:
            continue
        if page is not None:
            yield page

def gen_corpus_chunks(html_corpus):
    soup = BeautifulSoup.BeautifulSoup(html_corpus)
    for tag in soup.recursiveChildGenerator():
        if tag.string is not None:
            yield tag.string

def plain_corpus(html_corpus):
    return ' '.join(gen_corpus_chunks(html_corpus))


