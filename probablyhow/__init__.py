from sys import argv
from probablyhow.markov import rand_sentences_from_pairs
from probablyhow.search import APICall

def howto():
    default_task = 'ask better questions'
    task = ' '.join(argv[1:]).strip()
    if not task:
        task = default_task

    call = APICall()
    pairs = call.query(task, default_task)
    results = rand_sentences_from_pairs(pairs, 5, 10)
    for i, x in enumerate(results, 1):
        print('{}: {}'.format(i, x.encode('utf8')))
