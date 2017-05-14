from probablyhow.markov import rand_sentences_from_query
from flask import Flask, redirect, render_template, request, url_for

#from pdb import set_trace; set_trace()
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return app.send_static_file('index.html')

#TODO Redirect doesn't seem to work for empty task
@app.route('/to')
def search():
    task = request.args.get('task', '').replace('+', '%20')
    text_results = rand_sentences_from_query(task, 5, 10)
    paired_results = (('IMAGE', text) for text in text_results)
    return render_template('results.html', task=task, steps=paired_results)

if __name__ == '__main__':
    app.run()
