from flask import Flask, render_template, request, url_for, redirect
from CF import similar_5movies

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
    # add back-end processing codes for search here #
    # input: search (string)
    # output: list of dictionary items, variables = title, year, director, cast, description 
    #################################################

    results = [
        {
            'title': 'Movie Title 1',
            'year': '2022',
            'director': 'Director 1',
            'cast': 'Cast1, Cast2',
            'description': 'Description 1'
        },

        {
            'title': 'Movie Title 2',
            'year': '2021',
            'director': 'Director 2',
            'cast': 'Cast1, Cast2',
            'description': 'Description 2'
        }
    ]
    length=len(results)

    ##########################################################
    # add back-end processing codes for recommendations here #
    # input: search (string)
    # output: list of dictionary items, variables = title, year, director, cast, description 
    ##########################################################
    #results = similar_5movies('Dirty Dancing (1987)')

    recommendations = [
        {
            'title': 'Movie Title 3',
            'year': '2020',
            'director': 'Director 3',
            'cast': 'Cast1, Cast2',
            'description': 'Description 3'
        },

        {
            'title': 'Movie Title 4',
            'year': '2019',
            'director': 'Director 4',
            'cast': 'Cast1, Cast2',
            'description': 'Description 4'
        }
    ]
    return render_template("results.html", search=search, length=length, results=results, recommendations=recommendations)

if __name__ == "__main__":
    app.run()