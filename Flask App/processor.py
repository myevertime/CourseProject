from CF import similar_5movies
from knowledge_graph import knowledge_graph
import pandas as pd
import time
from search_client import SearchClient

searcher = SearchClient('http://54.68.224.178', '8090')

def processor(keyword=''):

    start_time = time.time()
    search_result = searcher.search(keyword)
    if len(search_result) == 0:
        raise Exception("empty search result")

    print("--- %s seconds --- for search" % (time.time() - start_time))

    metadata = pd.read_csv("output_rendered.csv")

    ##### Search Results
    results = []
    for i in range(len(search_result)):
        result = {}
        result['title'] = metadata.loc[metadata['movieId'] == search_result[i], 'title'].item()
        result['genres'] = metadata.loc[metadata['movieId'] == search_result[i], 'genres'].item()
        result['director'] = metadata.loc[metadata['movieId'] == search_result[i], 'director'].item()
        result['actors'] = metadata.loc[metadata['movieId'] == search_result[i], 'actors'].item()
        results.append(result)

    ##### Recommendation Results
    ## Get MovieIDs for KG
    tmdb_id = str(metadata.loc[metadata['movieId'] == search_result[0], 'tmdbId'].item())
    imdb_id = str(metadata.loc[metadata['movieId'] == search_result[0], 'imdbId'].item())

    ## Get Top5 movie IDs from each model
    start_time = time.time()
    CF_reco = similar_5movies(search_result[0])
    print("--- %s seconds --- for CF" % (time.time() - start_time))

    start_time = time.time()
    kg_reco = knowledge_graph(tmdb_id, imdb_id)
    print("--- %s seconds --- for KG" % (time.time() - start_time))
    
    ## Map KG recommendation results to MovieID
    kg_reco_pro = []
    for i in kg_reco:
        if "tt" not in i:
            check = metadata.loc[metadata['tmdbId'] == int(i.replace("tt","")), 'movieId']
            if len(check) > 0: # If ID exists in output.csv
                kg_reco_pro.append(metadata.loc[metadata['tmdbId'] == int(i), 'movieId'].item())
        else:
            check = metadata.loc[metadata['imdbId'] == int(i.replace("tt","")), 'movieId']
            if len(check) > 0: # If ID exists in output.csv
                kg_reco_pro.append(metadata.loc[metadata['imdbId'] == int(i.replace("tt","")), 'movieId'].item())

    reco = list(CF_reco)
    reco.extend(x for x in kg_reco_pro if x not in reco) # extend without duplicates

    recommendations = []
    for i in range(len(reco)):
        result = {}
        result['title'] = metadata.loc[metadata['movieId'] == reco[i], 'title'].item()
        result['genres'] = metadata.loc[metadata['movieId'] == reco[i], 'genres'].item()
        result['director'] = metadata.loc[metadata['movieId'] == reco[i], 'director'].item()
        result['actors'] = metadata.loc[metadata['movieId'] == reco[i], 'actors'].item()
        recommendations.append(result)

    return results, recommendations

if __name__=='__main__':
    start_time = time.time()
    print(processor('jumanji'))
    print("--- %s seconds --- for main" % (time.time() - start_time))
