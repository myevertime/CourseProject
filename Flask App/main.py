from flask import Flask, render_template, request, url_for, redirect
from processor import processor

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search = request.form.get('search')
        return redirect(url_for('results', search=search))
    
    return render_template('index.html', search='')

@app.route("/results", methods=['GET', 'POST'])
def results():
    search = request.form.get('search') # this is the search term
    results, recommendations = processor(search)
    length=len(results)

    return render_template("results.html", search=search, length=length, results=results, recommendations=recommendations)

@app.errorhandler(Exception)
def server_error(err):
    app.logger.exception(err)
    return render_template("error.html")

if __name__ == "__main__":
    app.run()