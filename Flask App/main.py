from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form["name"]
        return redirect(url_for('results', name=name))
    return render_template('index.html')


@app.route("/results", methods=['GET', 'POST'])
def results():
    name = request.form.get('name')
    print(name)
    return render_template("results.html", name=name)

if __name__ == "__main__":
    app.run()