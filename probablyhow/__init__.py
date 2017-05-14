from sys import argv
from probablyhow.markov import rand_sentences_from_query

def howto():
    query = ' '.join(argv[1:])
    results = rand_sentences_from_query(query, 5, 10)
    pairs = enumerate(results, 1)
    for i, x in pairs:
        print('{}: {}'.format(i, x.encode('utf8')))
