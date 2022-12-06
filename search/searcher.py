import metapy

movie_data_filename = "normalized_data.csv"

class Searcher:
    def __init__(self, cfg):
        self.inv_idx = metapy.index.make_inverted_index(cfg)
        self.ranker = metapy.index.OkapiBM25()
        print('make make_inverted_index')
        print('num docs:', self.inv_idx.num_docs())
        print('num vocabularies:', self.inv_idx.unique_terms())
        print('avg doc len', self.inv_idx.avg_doc_length())
        print('total corpus terms:', self.inv_idx.total_corpus_terms())

    def find_movie(self,filename, idx):
        cnt = 0
        with open(filename, 'r') as f:
            for line in f:
                if (idx == cnt):
                    return line.split(",")
                else:
                    cnt = cnt + 1

    def search(self,raw_query):
        query = metapy.index.Document()
        query.content(raw_query)
        top_docs = self.ranker.score(self.inv_idx, query, num_results=10)
        results = []
        for _, (d_id, _) in enumerate(top_docs):
            content = self.find_movie(movie_data_filename, d_id+1)
            movie_id = content[0]
            results.append(int(movie_id))
        return {"movieIds": results}

if __name__ == '__main__':
    searcher = Searcher('config.toml')

    while True:
        print('\n========Search: ')
        user_query_text = input()

        print(searcher.search(user_query_text))
