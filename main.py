from dotenv import load_dotenv
import os

from seleniumwire import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep

import requests
from bs4 import BeautifulSoup
from time import sleep
import re
import pandas as pd
from fake_useragent import UserAgent


# - step1 selenium 上網登入 ee-class
url = "https://ncueeclass.ncu.edu.tw/" # = ee-class url

# : load the env variable
env_account = os.getenv("EE_CLASS_ACCOUNT") # = 獲取環境變數
env_password = os.getenv("EE_CLASS_PASSWORD") # = 獲取環境變數

# : user agent setting
ua = UserAgent()
user_agent = ua.random

# : option setting
chrome_opt = Options()
chrome_opt.add_argument("start-maximized")  # 開啟視窗最大化
chrome_opt.add_argument("--disable-proxy-certificate-handler")
chrome_opt.add_argument("--disable-content-security-policy")
chrome_opt.add_argument("--disable-proxy-certificate-handler")
chrome_opt.add_argument("--ignore-certificate-errors")
chrome_opt.add_argument("--incognito")      # 設置隱身模式，可以避免個人化廣告，加速網頁瀏覽

# : driver setting 
driver = webdriver.Chrome(options = chrome_opt) # => insert the option to the driver (can be overridden)
driver.delete_all_cookies() # 防止污染

# @ Working to login
driver.get(url)
driver.implicitly_wait(5)  

account_input = driver.find_element(By.ID, "account")
password_input = driver.find_element(By.ID, "password")
# login_button = driver.find_element(By.CSS_SELECTOR, "button.btn-primary.btn-lg.btn-block") # = 找到登入按鈕

# account_input.send_keys(env_account)
# password_input.send_keys(env_password)
# login_button.click()
driver.implicitly_wait(10)  


