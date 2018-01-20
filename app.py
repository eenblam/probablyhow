from probablyhow.markov import rand_steps_from_pairs
from probablyhow.search import APICall
from probablyhow.util import CannotCompleteRequestError
from probablyhow.suggestions import random_task
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html', suggested_task=random_task())

@app.route('/to')
def search():
    default_task = 'ask better questions'
    original_task = request.args.get('task', '').replace('+', '%20').strip()
    task = original_task if original_task else default_task

    call = APICall()
    try:
        pairs = call.query(task)
    except CannotCompleteRequestError:
        try:
            pairs = call.query(default_task)
        except:
            return 500

    steps = rand_steps_from_pairs(pairs, 140, 5, 10)
    enum_steps = ((i, title, text) for i, (title, text) in enumerate(steps, 1))
    return render_template('results.html', task=task, steps=enum_steps)

if __name__ == '__main__':
    app.run()
