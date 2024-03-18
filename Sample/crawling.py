from bs4 import BeautifulSoup
import time
import requests
import json
from collections import deque
import re

import time

def ncu_crawl(url):
    try:
        resp = requests.get(url = url)
        if resp.status_code != 200:
            print('Invalid url:', resp.url)
            return '', '', []

        soup = BeautifulSoup(resp.text,"html.parser")

        # 獲取標題（title）
        title = soup.title
        title = title.string if title else ''

        # 獲取所有文字內容
        content = soup.get_text().strip()
        content = re.sub(r'\n+', '\n', content)

        # 獲取所有links
        links = []
        all_links = soup.find_all(href=True)
        for link in all_links:
            href = link.get('href')
            if href:
                if "http" not in href:
                    if href[0]!="/":
                        href = f"{root_url}/{href}"
                    else:
                        href = root_url + href
                text = link.get_text().strip()
                if text == '':
                    text = link.get('title','').strip()

                links.append((text,href))
        time.sleep(0.5)
        return title, content, links
    except:
        return '', '', []

def bfs_crawl(root_url, max_depth):
    visited = set()
    queue = deque([(root_url, 0)])
    results = []

    while queue:
        current_url, depth = queue.popleft()

        # 停止條件：達到指定的最大深度
        if depth > max_depth:
            break

        # 如果該 URL 已經訪問過，跳過
        if current_url in visited:
            continue

        # 獲取該 URL 的所有超連結
        title, content, links = ncu_crawl(current_url)

        if title and content and links:
            print("Depth:", depth, "URL:", current_url)

            # 將所有未訪問過的超連結加入隊列，並更新深度
            for text, link in links:
                if link not in visited:
                    queue.append((link, depth + 1))

            # 標記當前 URL 為已訪問
            visited.add(current_url)
            results.append({'url': current_url, 'title': title, 'depth':depth, 'content': content, 'links': links})
    return results


if __name__ == '__main__':

    start_time = time.time()

    filename = 'result.json'
    root_url = 'http://lrn.ncu.edu.tw/'
    max_depth = 2
    crawl_results = bfs_crawl(root_url, max_depth)

    with open(filename, 'w', encoding='utf-8') as f:    
        json.dump(crawl_results, f, ensure_ascii=False, indent=4)
        print(f"{len(crawl_results)} of data were successfully saved")
        
        
    # @ Done
    end_time = time.time()
    print(f"總共花費時間：{end_time - start_time}秒")