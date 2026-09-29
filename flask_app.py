import base64
from io import BytesIO
from flask import Flask, render_template, request

# CRITICAL FOR PYTHONANYWHERE: Use the non-interactive Agg backend
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import wordle_counts as wc

counts = wc.get_letter_counts(wc.answers)

def plot_graph(x_values, y_values):
    plt.plot(x_values,y_values)
    # 3. Use plt.gca() to target the y-axis and set the major locator
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(10))

    plt.title(f"Counts last updated on {wc.last_date}")
    for x, y in zip(x_values, y_values):
        plt.annotate(f'({x},{y})', xy=(x,y), xytext=(x,y))
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close() # Clear the current figure memory
    buf.seek(0)
    plot_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return plot_base64

app = Flask(__name__)

@app.route('/')
def index():

    letter_counts = [sum(counts[index]) for index, letter in enumerate(wc.letters)]
    plot_base64 = plot_graph(wc.letters, letter_counts)

    return render_template('index.html', plot_var=plot_base64)

@app.route('/plot_beginnning_counts', methods=['POST'])
def plot_beginnning_counts():
    beginning_letter_counts = [counts[index][0] for index, letter in enumerate(wc.letters)]
    plot_base64 = plot_graph(wc.letters, beginning_letter_counts)

    return render_template('index.html', plot_var=plot_base64)

@app.route('/show_counts', methods=['POST'])
def show_counts():
    letter = request.form['letter_name']
    i = wc.letters.index(letter)
    letter_counts = counts[i]
    positions = ['first', 'second', 'third', 'fourth', 'last']
    plot_base64 = plot_graph(positions, letter_counts)

    return render_template('index.html', plot_var=plot_base64)


@app.route('/get_dates', methods=['POST'])
def get_dates():
    
    return render_template('user_input.html', last_date=wc.last_date_val)

@app.route('/show_dates', methods=['GET','POST'])
def start_and_end_dates():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    custom_answers = wc.get_answers_between_dates(wc.df, start_date, end_date)
    custom_counts = wc.get_letter_counts(custom_answers)
    custom_letter_counts = [custom_counts[index][0] for index, letter in enumerate(wc.letters)]
    plot_base64 = plot_graph(wc.letters, custom_letter_counts)
    
    return render_template('user_input.html', last_date=end_date, plot_var=plot_base64)
''' '''

if __name__ == '__main__':
    app.run(debug=True)