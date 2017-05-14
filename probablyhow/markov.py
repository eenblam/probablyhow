from random import randint

import markovify

from search import gen_pairs_from_query

def get_corpus(query):
    pairs = gen_pairs_from_query(query)
    texts = (x for _,x in pairs)
    return ' '.join(texts)

def model_from_query(query):
    corpus = get_corpus(query)
    return markovify.Text(corpus)

def rand_sentences_from_query(query, min_count, max_count):
    model = model_from_query(query)
    count = randint(min_count, max_count)
    for _ in range(count):
        yield model.make_sentence()

def rand_step(model, char_count, max_sentences):
    count = randint(1, max_sentences)
    title = model.make_short_sentence(char_count)
    text = ' '.join(model.make_sentence() for _ in range(count))
    return title, text

def rand_steps_from_query(query, title_count, min_sentences, max_sentences):
    model = model_from_query(query)
    count = randint(min_sentences, max_sentences)
    for _ in range(count):
        yield rand_step(model, title_count, max_sentences)
