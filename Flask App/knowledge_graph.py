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
    #Rank, format and return the top 10 results            
    temp_list = [[i["movieLabel"],i["movie_id"],i["rank"]] for i in r_list]
    r_list.clear() #clear the original r_list
    for i, g in groupby(sorted(temp_list), key=lambda x: x[0:2]):
        r_list.append([i,sum(v[2] for v in g)])
    recommendations = [i[0] for i in sorted(r_list, key=lambda l:l[1], reverse=True)][:10]
    return recommendations #return movie title + id (imdb id if exists, else tmdb id)

if __name__ == '__main__':
    #Example (The Terminator)
    r_list = knowledge_graph('218', '0088247') 
    for i in r_list:
        print(i[0],i[1])