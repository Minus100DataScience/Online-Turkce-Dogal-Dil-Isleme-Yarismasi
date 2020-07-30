from flask import Flask, render_template, request
from Test import user
from Test import add_tested
app = Flask('Syber_Bully_Finder')

textim = ""
pred = ""


@app.route('/')
def show_predict_bully_form():
    return render_template('predictorform.html')


@app.route('/result', methods=['POST'])
def results():
    form = request.form
    if request.method == 'POST':
        text = request.form['text']
        global textim
        textim = text
        bully = user(text)
        global pred
        pred = bully
        return render_template('resultsform.html', tweet=text, bully=bully)


@app.route('/react', methods=['POST'])
def reacts():
    form = request.form
    if request.method == 'POST':
        react = request.form['reaction']
        add_tested(react, textim, pred)
        return render_template('reactionform.html')


app.run("localhost", "9999", debug=True)
