from collections import namedtuple
from re import sub

import BeautifulSoup

from util import CannotCompleteRequestError

Page = namedtuple('Page', ['title', 'text'])

def process_title_response(response):
    """Produce a title string from results of initial search

    Just fetch the first 10, ignoring pagination
    """
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
    """Retrieve pageids from response to query for title string, then yield each"""
    try:
        pages = response['query']['pages']
        keys = pages.keys()
    except KeyError:
        raise CannotCompleteRequestError('Cannot generate pageids from response')
    except AttributeError:
        raise CannotCompleteRequestError('Cannot generate pageids from response')
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

def strip_tags(html_corpus):
    """Strip HTML tags from article text"""
    soup = BeautifulSoup.BeautifulSoup(html_corpus)
    strings = (tag.string for tag in soup.recursiveChildGenerator()
               if tag.string is not None)
    return ' '.join(strings)

def remove_button_text(article):
    """Remove artifacts of buttons from article markup
    
    A rather unfortunate hack
    """
    bad_strings = ['Edit Edit', 'Warnings Warnings', 'Steps Steps']
    for bad_string in bad_strings:
        pat = ' ?{} ?'.format(bad_string)
        article = sub(pat, ' ', article)
    return article

def clean_corpus(html_corpus):
    """Clean HTML tags and button text from articles"""
    return remove_button_text(strip_tags(html_corpus))
