from seleniumwire import webdriver  
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# - step1 selenium 上網登入 ee-class
url = "https://military.ncu.edu.tw" # = ee-class url

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

print("Try to change the page...")
# driver.find_element(By.ID, "nav-link").click()
nav_link = driver.find_element(By.ID, "nav-link")
driver.execute_script("arguments[0].click();", nav_link)

# : Get the Cookies & Headers
current_login_cookie = driver.get_cookies()
current_login_requests = driver.requests

headers = {}
for request in driver.requests:
    if request.url == "https://military.ncu.edu.tw":
        headers = {k: v for k, v in request.headers.items()}

print("Cookies:", current_login_cookie)
print("Headers:", headers)

sleep(5)
driver.quit()