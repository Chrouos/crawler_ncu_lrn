import traceback

from seleniumwire import webdriver  
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep, time

import requests
from bs4 import BeautifulSoup
from collections import deque
import re
import json

def reload_cookies(url, type_value="bs4"):
    
    # : user agent setting
    ua = UserAgent()
    user_agent = ua.random

    # : option setting
    chrome_opt = Options()
    chrome_opt.add_argument("start-maximized")  # 設定瀏覽器啟動時開啟視窗最大化，提供較大的視野和操作空間
    chrome_opt.add_argument("--disable-proxy-certificate-handler")  # 禁用代理伺服器的證書處理，避免因證書問題而影響網頁載入
    chrome_opt.add_argument("--disable-content-security-policy")  # 禁用內容安全政策(CSP)，允許加載非同源的腳本，有助於測試開發
    chrome_opt.add_argument("--ignore-certificate-errors")  # 忽略證書錯誤，有助於訪問自簽名證書的開發環境或測試站點
    chrome_opt.add_argument("--incognito")  # 啟動無痕(隱身)模式，不會保存瀏覽歷史、Cookies等資料，有助於保護隱私和測試

    # : driver setting 
    driver = webdriver.Chrome(options = chrome_opt) # => insert the option to the driver (can be overridden)
    driver.delete_all_cookies() # 防止污染
    driver.get(url)
    sleep(2)

    # # : driver get the title, content, links
    # driver_title = driver.title if type == "selenium" else ""
    # driver_content = driver.find_element(By.TAG_NAME, "body").text if type == "selenium" else ""
    # driver_all_links_elements = driver.find_elements(By.XPATH, "//a[@href]") if type == "selenium" else ""

    # : Get the Cookies & Headers
    current_login_cookie = driver.get_cookies()
    current_login_requests = driver.requests

    headers = {}
    for request in current_login_requests:
        if request.url == url:
            headers = {k: v for k, v in request.headers.items()}

    # print("Cookies:", current_login_cookie)
    # print("Headers:", headers)

    sleep(5)
    if type_value == "bs4": driver.quit()
    
    return current_login_cookie, headers, driver

def crawl_ncu_bs4(url, cookies, headers):
    try:
        with requests.Session() as session: 
        # ~ Session can update the performance of the server. 
    
            # : Update the Cookies & Headers from driver
            for cookie in cookies:
                session.cookies.set(cookie['name'], cookie['value'])
            session.headers.update(headers)
        
            # :  Get the response of the website.
            resp = session.get(url)
            
            # @ Check the response and Parser the response to HTML.
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            
            # @ Get the elements of the site.
            title = soup.title.get_text() if soup.title else ''
            
            content = soup.get_text().strip()
            content = re.sub(r'\n+', '\n', content)
            
            links = []
            all_links = soup.find_all(href=True)
            for link in all_links:
                href = link.get('href') 
                text = link.get_text().strip()

                # @ Get the Link and Href from the link
                if href:
                    if "http" not in href: 
                        href = f"{url}/{href}" if href[0] != "/" else f"{url}{href}" # = href that include the relative path
                    
                    if text == "": 
                        text = link.get('title','').strip()
                    
                    links.append((text,href))
            
        sleep(1)
        return title, content, links
    except requests.HTTPError as e:
        print('HTTP error', e.response.status_code, url)
    except requests.RequestException as e:
        print('Request error:', e)
    except Exception as e:
        traceback.print_exc()
        print("Exception:", e)
        
    return '', '', []

def crawl_ncu_selenium(url):
    
    _, _, driver = reload_cookies(url, type_value="selenium")
    
    # : driver get the title, content, links
    driver_title = driver.title 
    driver_content = driver.find_element(By.TAG_NAME, "body").text 
    driver_all_links_elements = driver.find_elements(By.XPATH, "//a[@href]") 
    
    links = []
    for element in driver_all_links_elements:
        
        href = element.get_attribute('href')
        text = element.text.strip()

        if href:
            # 確保連結是完整的 URL
            if "http" not in href:
                href = f"{url}/{href}" if href[0] != "/" else f"{url}{href}"

            if text == "":
                # 如果連結文本為空，嘗試獲取 title 屬性
                text = element.get_attribute('title').strip()

            links.append((text, href))
            
    driver.quit()
    return driver_title, driver_content, links

def crawl_bfs(root_url, max_depth, type_value="bs4"):
    '''
        return  {   
                    url: string,
                    title: string,
                    depth: int,
                    content: string,
                    links: [(string, string)]
                }
    '''

    # : default setting
    visited = set() 
    results = []
    
    current_url, depth = root_url, 0
    cookies, headers, _ = reload_cookies(root_url) if type_value == "bs4" else ("", "", {})
    dq = deque([(current_url, depth)]) # = 暫存器
    
    while dq:
        try:
            current_url, depth = dq.popleft() 
        
            if depth > max_depth: break # + 停止條件：達到指定的最大深度
            if current_url in visited: continue # + 如果該 URL 已經訪問過，跳過
            
            # @ Get the elements of the site. (all the links)
            title, content, links = crawl_ncu_bs4(current_url, cookies, headers) if type_value == "bs4" else crawl_ncu_selenium(current_url)
            if title and content and links:
                print("Depth:", depth, "URL:", current_url)
                    
                # @ 將所有未訪問過的超連結加入隊列，並更新深度
                for text, link in links:
                    if link not in visited: dq.append((link, depth + 1))
                    
                # @ Done
                visited.add(current_url)
                results.append({'url': current_url, 'title': title, 'depth':depth, 'content': content, 'links': links})
        
        except Exception as e:
            traceback.print_exc()
            cookies, headers, _ = reload_cookies(root_url) if type_value == "bs4" else ("", "", {})
            
            print(e)
            
    return results

if __name__ == "__main__":
    
    # @ Start
    start_time = time.time()
    
    # : default setting
    root_url = "http://lrn.ncu.edu.tw/"
    save_file_name = "result.json"
    max_depth = 2
    
    print(f"=> 存檔名稱: {save_file_name}, 爬取的網站: {root_url}, 深度: {max_depth}")
    
    # @ main function
    crawlers_results =  crawl_bfs(root_url, max_depth, type_value="bs4") # type_value="selenium" or "bs4"
    
    with open(save_file_name, 'w', encoding='utf-8') as f:    
        json.dump(crawlers_results, f, ensure_ascii=False, indent=4)
        print(f"{len(crawlers_results)} of data were successfully saved")
        
    # @ Done
    end_time = time.time()
    print(f"總共花費時間：{end_time - start_time}秒")

        
    
    
    