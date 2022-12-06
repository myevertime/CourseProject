import requests

class SearchClient:
    def __init__(self, url, port):
       self.url = url 
       self.port = port
    
    def search(self, raw_query):
        payload = {'keyword': raw_query}
        r = requests.get(f'{self.url}:{self.port}/search', params=payload)
        return r.json()['movieIds']
