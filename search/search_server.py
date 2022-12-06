from bottle import route, run, template, request
from searcher import Searcher

searcher = Searcher('config.toml')
print(searcher)

@route('/search')
def index():
    keyword = request.query.keyword
    return searcher.search(keyword)

run(host='localhost', port=8090)
