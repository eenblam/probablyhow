from sys import argv
from probablyhow.markov import rand_sentences_from_pairs
from probablyhow.search import APICall
from probablyhow.util import CannotCompleteRequestError

def howto():
    default_task = 'ask better questions'
    original_task = ' '.join(argv[1:]).strip()
    task = original_task if original_task else default_task

    call = APICall()
    try:
        pairs = call.query(task)
    except CannotCompleteRequestError:
        try:
            pairs = call.query(default_task)
        except:
            print('Cannot complete request: {}'
                    .format(original_task))

    results = rand_sentences_from_pairs(pairs, 5, 10)
    for i, x in enumerate(results, 1):
        print('{}: {}'.format(i, x.encode('utf8')))
