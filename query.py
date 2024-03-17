from elasticsearch import Elasticsearch
import json
import sys
from pprint import pprint

def query(item, query):
    
    # : Connect Setting
    index_name = 'ncu_math' # = create name.
    es = Elasticsearch(hosts=["http://localhost:9200"])
    
    type = 'one_to_one'

    # Query DSL
    search_params = {
        "query": {
            "match": {item: q}
        }
    }
    
    #Search document
    result = es.search(index=index_name, body=search_params, size=1, from_=0)
    
    return result['hits']['hits']

if __name__ == "__main__":   
    # item, q = sys.argv[1], sys.argv[2]  
    item = 'content'
    q = input("your query:")
    results = query(item, q) 
    for res in results:
        print(res['_score']) 
        print(res['_source']['url'])
    
    