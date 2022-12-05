import metapy
import json

inv_idx = metapy.index.make_inverted_index('config.toml')
ranker = metapy.index.OkapiBM25()
movie_data = open('normalized_data.csv', 'r').readlines()

def search(raw_query):
    query = metapy.index.Document()
    query.content(raw_query)
    top_docs = ranker.score(inv_idx, query, num_results=5)
    results = []
    for _, (d_id, _) in enumerate(top_docs):
        content = movie_data[d_id+1].split(",")
        movie_id = content[0]
        results.append(int(movie_id))
    return results

if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print("Usage: {} config.toml".format(sys.argv[0]))
    #     sys.exit(1)
    
    # cfg = sys.argv[1]
    # print('Building or loading index...')
    inv_idx = metapy.index.make_inverted_index('config.toml')
    print('num docs:', inv_idx.num_docs())
    print('num vocabularies:', inv_idx.unique_terms())
    print('avg doc len', inv_idx.avg_doc_length())
    print('total corpus terms:', inv_idx.total_corpus_terms())

    ranker = metapy.index.OkapiBM25()

    while True:
        print('\n========Search: ')
        user_query_text = input()

        print(search(user_query_text))
