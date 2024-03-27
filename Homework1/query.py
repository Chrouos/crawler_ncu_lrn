from elasticsearch import Elasticsearch
import json
import sys
from pprint import pprint

from sentence_embedding import get_sentence_embedding #, cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def vector_search(item, query_vector, index_name, es, query_size=2):
    query_vector = q_embedding.tolist()  # 將張量轉換為列表
    search_params = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        }
    }
    
    result = es.search(index=index_name, body=search_params, from_=0, size=query_size)
    return result['hits']['hits']

def query(item, query, index_name, es, query_size=2):
    
    # Query DSL
    search_params = {
        "query": {
            "match": {item: query}
        }
    }
    
    #Search document
    result = es.search(index=index_name, body=search_params, from_=0, size=query_size)
    
    return result['hits']['hits']

if __name__ == "__main__":   
    
    # : Connect Setting
    index_name = 'ncu_lrn' # = create name.
    es = Elasticsearch(hosts=["http://localhost:9200"])
    
    # : Query Setting
    query_size = 2
    item = 'content'
    q = input("your query:") 
    # q = "張立杰教授的個人簡例和研究計畫"
    q_embedding = get_sentence_embedding(q)
    results = query(item, q, index_name, es, query_size) 
    
    print("搜尋語句:", q, "搜尋欄位:", item)
    print("------------------------------------------------")
    
    contents = []
    urls = []
    
    print("未使用 Embedding 搜尋結果:")
    for res in results:
        print("URL:", res["_source"]['url'])
        contents.append(res["_source"]['content'])
        urls.append(res["_source"]['url'])
        
    print("@ 使用 Embedding 搜尋結果:")
    results = vector_search(item, q_embedding, index_name, es, query_size)
    for res in results:
        print("URL:", res["_source"]['url'])
        contents.append(res["_source"]['content'])
        urls.append(res["_source"]['url'])
        
    max_url = urls[0]
    max_score = 0
    
    vectorizer = TfidfVectorizer()
    all_texts = contents + [q]
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # 計算與q的相似度
    for r in range(len(urls)):
        score = cosine_similarity(tfidf_matrix[r], tfidf_matrix[-1])[0,0]
        if score > max_score:
            max_score = score
            max_url = urls[r]
            
    print("--------")
    print("sklearn output:", max_url)
    
    
    