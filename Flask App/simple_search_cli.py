import metapy
import pytoml
import sys


def print_docs(inv_idx, top_docs):
    for num, (d_id, _) in enumerate(top_docs):
        content = inv_idx.metadata(d_id).get('content')
        print("{}. {}...\n".format(num + 1, content[0:250]))

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

        query = metapy.index.Document()
        query.content(user_query_text)

        top_docs = ranker.score(inv_idx, query, num_results=5)
        print('results: \n')
        print_docs(inv_idx, top_docs)
