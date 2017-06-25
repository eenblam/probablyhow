import BeautifulSoup
import requests

url = 'https://www.wikihow.com/api.php'
headers = {
        'User-Agent': 'ProbablyHow User Agent',
        'From': 'github.com/eenblam/probablyhow/issues'
    }

data_query = {
        'format': 'json',
        'action': 'query',
        'list': 'search',
        'srwhat': 'text'
    }

data_titles = {
        'format': 'json',
        'action': 'query',
        'export': True
    }

data_parse = {
        'format': 'json',
        'action': 'parse',
        'prop': 'text'
    }

def title_string_from_query(query):
    default_query = 'ask better questions'
    query = query if query.strip() else default_query
    params = {'srsearch': query}
    params.update(data_query)
    j = requests.get(url, params, headers=headers).json()
    titles = [x['title'] for x in j['query']['search']]
    if titles:
        return '|'.join(titles)
    else:
        # Handle this in the worst way possible
        return title_string_from_query(default_query)

def titles_to_pageids(title_string):
    """Get pageids from title string"""
    params = {'titles': title_string}
    params.update(data_titles)
    del params['export']
    r = requests.get(url, params, headers=headers).json()
    for pageid in r['query']['pages'].keys():
        yield pageid

def get_page_by_id(pageid):
    params = {'pageid': pageid}
    params.update(data_parse)
    return requests.get(url, params, headers=headers).json()

def get_pairs(title_string):
    result_stream = (get_page_by_id(pageid)['parse'] for pageid
            in titles_to_pageids(title_string))
    text_stream = ((x['title'], x['text']['*']) for x in result_stream)
    clean_stream = ((title, plain_corpus(text)) for title, text in text_stream)
    return clean_stream

def _gen_plain_corpus(html_corpus):
    soup = BeautifulSoup.BeautifulSoup(html_corpus)
    for tag in soup.recursiveChildGenerator():
        if tag.string is not None:
            yield tag.string

def plain_corpus(html_corpus):
    return ' '.join(_gen_plain_corpus(html_corpus))

def gen_pairs_from_query(query):
    titles = title_string_from_query(query)
    pairs = get_pairs(titles)
    return pairs
