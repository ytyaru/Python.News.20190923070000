from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from bs4 import Comment
import time
import re

def get_html(url, wait_second=1):
    html = __get_more_link(__get_html(url))
    html = __del_element(html)
    time.sleep(wait_second)
    return html

def __get_html(url):
    options = Options()
    options.set_headless(True)
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    return driver.page_source.encode('utf-8').decode('utf-8')

# 「続きを読む」リンクがあるならそのURLを返す。なければ元のURLを返す
def __get_more_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    link = soup.find('a', text=re.compile(r'^.*続きを読む.*$'))
    return html if link is None else __get_html(link.get('href'))

# 不要な要素を削除する
def __del_element(html):
    soup = BeautifulSoup(html, 'html.parser')
    soup.find('head').decompose()
    for comment in soup(text=lambda x: isinstance(x, Comment)): comment.extract()
    for script in soup.find_all('script', src=False): script.decompose()
    for noscript in soup.find_all('noscript'): noscript.decompose()
    return str(soup.html)

