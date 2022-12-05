from pywikibot.data.sparql import SparqlQuery
from string import Template
import glob
from itertools import groupby

def knowledge_graph(tmdb_id, imdb_id):
    wikiquery = SparqlQuery()
    r_list = []
    for i in glob.glob('./queries/*.rq'):
        with open(i, 'r') as query_file:
            query = query_file.read()
        #Subsitute variables
        temp = Template(query)
        query = temp.safe_substitute(TMDB = tmdb_id, IMDB = imdb_id)
        #Execution
        try:
            q_result=wikiquery.select(query)
            [v.update(rank=1/(i+1)) for i,v in enumerate(q_result)]
            r_list.extend(q_result)
        except Exception as e:
            print(e)
    #Rank, format and return the top 5 results
    temp_list = [[i["movie_id"],i["rank"]] for i in r_list]
    r_list.clear() #clear the original r_list
    for i, g in groupby(sorted(temp_list), key=lambda x: x[0]):
        r_list.append([i,sum(v[1] for v in g)])
    recommendations = [i[0] for i in sorted(r_list, key=lambda l:l[1], reverse=True)][:5]
    return recommendations #return ids (imdb_id if exists, else tmdb_id)

if __name__ == '__main__':
    #Example (The Terminator)
    r_list = knowledge_graph('218', '0088247') 
    for i in r_list:
        print(i)
