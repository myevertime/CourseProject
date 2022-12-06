import metapy
import json

inv_idx = metapy.index.make_inverted_index('config.toml')
ranker = metapy.index.OkapiBM25()
movie_data_filename = "normalized_data.csv"

def find_movie(filename, idx):
    cnt = 0
    with open(filename, 'r') as f:
        for line in f:
            if (idx == cnt):
                return line.split(",")
            else:
                cnt = cnt + 1

def search(raw_query):
    query = metapy.index.Document()
    query.content(raw_query)
    print('before')
    top_docs = ranker.score(inv_idx, query, num_results=5)
    print('after')
    results = []
    for _, (d_id, _) in enumerate(top_docs):
        content = find_movie(movie_data_filename, d_id+1)
        movie_id = content[0]
        results.append(int(movie_id))
    return results

# if __name__ == '__main__':
#     # if len(sys.argv) != 2:
#     #     print("Usage: {} config.toml".format(sys.argv[0]))
#     #     sys.exit(1)
    
#     # cfg = sys.argv[1]
#     # print('Building or loading index...')
#     inv_idx = metapy.index.make_inverted_index('config.toml')
#     print('make make_inverted_index')
#     print('num docs:', inv_idx.num_docs())
#     print('num vocabularies:', inv_idx.unique_terms())
#     print('avg doc len', inv_idx.avg_doc_length())
#     print('total corpus terms:', inv_idx.total_corpus_terms())

#     ranker = metapy.index.OkapiBM25()

#     while True:
#         print('\n========Search: ')
#         user_query_text = input()

#         print(search(user_query_text))
