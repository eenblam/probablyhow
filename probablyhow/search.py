import requests

import process
from util import RequestError

class APICall(object):
    def __init__(self):
        self.url = 'https://www.wikihow.com/api.php'
        self.headers = {
            'User-Agent': 'ProbablyHow User Agent',
            'From': 'github.com/eenblam/probablyhow/issues'
        }

    def get_JSON(self, params):
        try:
            r = requests.get(self.url, params, headers=self.headers)
        except requests.exceptions.ConnectionError:
            #TODO WikiHow is down or network is down
            # "That's weird. We can't talk to WikiHow. We're looking into it."
            raise RequestError("Couldn't connect to WikiHow")

        #TODO Check status codes
        # WikiHow doesn't use r.status_code to communicate about results
        # if not r.ok bail
        # if r.status_code not 200, log r.status_code0

        try:
            # Got a response, but can't parse it
            deserialized = r.json()
        except ValueError:
            raise RequestError(
                    "Couldn't deserialize response from WikiHow",
                    url=r.request.url)
        return deserialized

    def search_for_titles(self, query):
        params = {
            'format': 'json',
            'action': 'query',
            'list': 'search',
            'srwhat': 'text',
            'srsearch': query.strip()
        }
        r = self.get_JSON(params)
        return process.process_title_response(r)

    def get_pageids_from_title_string(self, title_string):
        """Get pageids from title string"""
        params = {
            'format': 'json',
            'action': 'query',
            'titles': title_string
        }
        return self.get_JSON(params)

    def get_page_by_id(self, pageid):
        params = {
            'format': 'json',
            'action': 'parse',
            'prop': 'text',
            'pageid': pageid
        }
        return self.get_JSON(params)

    def get_pages_by_id(self, pageids):
        """Yield pages successfully retrieved"""
        for pageid in pageids:
            try:
                page = self.get_page_by_id(pageid)
            except RequestError as e:
                # It's okay to drop a page. Log it and move on.
                #TODO Check for e.url and log 
                continue
            yield page

    def query(self, query, backup_query):
        """Return generator of (title,text) pairs"""
        title_string = self.search_for_titles(query)
        if title_string == '':
            title_string = self.search_for_titles(backup_query)

        pageid_response = self.get_pageids_from_title_string(title_string)
        pageids = process.process_pageid_response(pageid_response)
        results = self.get_pages_by_id(pageids)

        text_stream = process.process_page_stream(results)
        clean_stream = ((title, process.plain_corpus(text))
                        for title, text in text_stream)
        # lol "clean." It's not. Someone please XSS me via WikiHow before I fix this.
        return clean_stream
