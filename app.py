from probablyhow.markov import rand_steps_from_pairs
from probablyhow.search import APICall
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/to')
def search():
    default_task = 'ask better questions'
    task = request.args.get('task', '').replace('+', '%20').strip()
    if not task:
        task = default_task

    call = APICall()
    pairs = call.query(task, default_task)
    steps = rand_steps_from_pairs(pairs, 140, 5, 10)
    enum_steps = ((i, title, text) for i, (title, text) in enumerate(steps, 1))
    return render_template('results.html', task=task, steps=enum_steps)

if __name__ == '__main__':
    app.run()
