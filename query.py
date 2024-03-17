from elasticsearch import Elasticsearch
import json
import sys
from pprint import pprint

def query(item, query, index_name, es):
    
    # Query DSL
    search_params = {
        "query": {
            "match": {item: query}
        }
    }
    
    #Search document
    result = es.search(index=index_name, body=search_params, from_=0, size=2)
    
    return result['hits']['hits']

if __name__ == "__main__":   
    # item, q = sys.argv[1], sys.argv[2]  
    
    # : Connect Setting
    index_name = 'ncu_lrn' # = create name.
    es = Elasticsearch(hosts=["http://localhost:9200"])
    
    item = 'content'
    q = input("your query:")
    results = query(item, q, index_name, es) 
    # print(results)
    
    for res in results:
        print("URL:", res["_source"]['url'])
    
    