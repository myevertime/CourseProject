from flask import Flask, render_template, request, url_for, redirect
#from processor import processor

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search = request.form["search"]
        return redirect(url_for('results', search=search))
    return render_template('index.html')

@app.route("/results", methods=['GET', 'POST'])
def results():
    search = request.form.get('search') # this is the search term

    #################################################
    # comment out the dummy results and recommendations lists
    # uncomment the following 2 lines:
    # from processor import processor
    # results, recommendations = processor(search)
    #################################################

    results = [
        {
            'title': 'Movie Title 1',
            'genre': 'adventure',
            'director': 'Director 1',
            'actors': 'Cast1, Cast2',
        },

        {
            'title': 'Movie Title 2',
            'genre': 'thriller',
            'director': 'Director 2',
            'actors': 'Cast1, Cast2',
        }
    ]

    recommendations = [
        {
            'title': 'Movie Title 3',
            'year': '2020',
            'director': 'Director 3',
            'actors': 'Cast1, Cast2',
        },

        {
            'title': 'Movie Title 4',
            'year': '2019',
            'director': 'Director 4',
            'actors': 'Cast1, Cast2',
        }
    ]

    #results, recommendations = processor(search)
    length=len(results)

    return render_template("results.html", search=search, length=length, results=results, recommendations=recommendations)

if __name__ == "__main__":
    app.run()