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


# - selenium 上網登入 ee-class
ua = UserAgent()
user_agent = ua.random

chrome_opt = Options()
chrome_opt.add_argument("start-maximized")  # 開啟視窗最大化
chrome_opt.add_argument("--incognito")      # 設置隱身模式，可以避免個人化廣告，加速網頁瀏覽