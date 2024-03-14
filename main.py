from bs4 import BeautifulSoup
import time
import requests
import json
from collections import deque
import re


def crawl_ncu(url):
    try:
        resp = requests.get(url = url)
        
    except Exception as e:
        print(e)


def crawl_bfs(root_url, max_depth):
    '''
        return  {   
                    url: string,
                    title: string,
                    depth: int,
                    content: string,
                    links: string
                }
    '''

    # : default setting
    visited = set() 
    results = []
    
    dq = deque([(root_url, 0)]) # = 暫存器
    
    while dq:
        current_url, depth = dq.popleft()
        
        # + 停止條件：達到指定的最大深度
        if depth > max_depth: break
        
        # + 如果該 URL 已經訪問過，跳過
        if current_url in visited: continue
        
        # @ 獲取該 URL 的所有 Link & URL
        # title, coutent, links = ncu_crawl(current_url)
        
        # @ Done
        visited.add(current_url)
        


if __name__ == "__main__":
    
    # : default setting
    group_of_ncu = "military" # = 爬蟲的組別 (生輔組: military)
    save_file_name = group_of_ncu + "_result.json" if group_of_ncu else "result.json"
    root_url = "https://" + (group_of_ncu if group_of_ncu else "www") + ".ncu.edu.tw"
    max_depth = 2
    
    print(f"=> 爬取網站類型: {group_of_ncu}, 存檔名稱: {save_file_name}, 爬取的網站: {root_url}")
    
    # : main function
    # root_crawlers_dict =  crawl_bfs(root_url, max_depth)
    
        
    
    
    