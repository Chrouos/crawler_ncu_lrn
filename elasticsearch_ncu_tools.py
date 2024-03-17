from elasticsearch import Elasticsearch, helpers
import json
import sys

'''
data = {
        'url': text,
        'title': text,
        'depth': integer,
        'content': text,
        'links': [tuple(text,text)]
    }
'''

hp_mapping = {
    "properties": {
        "url": {
            "type": "text"
        },
        "title": {
            "type": "text"
        },
        "depth": {
            "type": "integer"   
        },
        "content": {
            "type": "text"
        },
        "links": {
            "type": "text"
        }
    }
}

# Load dataset
def read_data(data_name):
    with open(data_name, 'r' ,encoding='utf-8') as f:
        data = json.load(f)
        for row in data:
            yield row

def delete_elasticsearch_index(index_name, es):
    
    # @ Delete Index
    if not es.indices.exists(index=index_name):
        print('Index not exists!')
    else:
        response = es.indices.delete(index=index_name, ignore=[400, 404])
        print('Delete Index:', response)

def load2_elasticsearch(index_name, es, data_name):

    # @ Create Index with mappings
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body={"mappings": hp_mapping})
        print('Index and mappings created!')
    else:
        print('Index already exists!')

    # @ Import data to elasticsearch
    success, _ = helpers.bulk(
        client=es, actions=read_data(data_name), index=index_name, ignore=400)
    print('Success: ', success)

if __name__ == "__main__":
    # : Connect Setting
    index_name = 'ncu_math' # = create name.
    es = Elasticsearch(hosts=["http://localhost:9200"])
    
    # delete_elasticsearch_index(index_name, es)
    load2_elasticsearch(index_name, es, data_name=f"math_result.json")