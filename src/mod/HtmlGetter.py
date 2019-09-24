from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from bs4 import Comment
import time
import re

class HtmlGetter:
#    def __init__(self): pass
#        self.__soup = BeautifulSoup(html, 'html.parser')
    def get(self, url, wait_second=1):
        self.__soup = BeautifulSoup(self.__get_html(url), 'html.parser')
#        self.__soup = BeautifulSoup(self.__get_html(url), 'lxml')
#        self.__soup = BeautifulSoup(__get_html(url), 'html.parser')
#        html = self.__get_more_link(__get_html(url))
        html = self.__get_more_link(str(self.__soup.html))
        html = self.__del_element(html)
        time.sleep(wait_second)
        return html
    def __get_html(self, url):
        options = Options()
        options.set_headless(True)
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
        return driver.page_source.encode('utf-8').decode('utf-8')
    # 「続きを読む」リンクがあるならそのURLを返す。なければ元のURLを返す
    def __get_more_link(self, html):
        link = self.__soup.find('a', text=re.compile(r'^.*続きを読む.*$'))
        return html if link is None else self.__get_html(link.get('href'))
    # 不要な要素を削除する
    def __del_element(self, html):
        self.__soup.find('head').decompose()
        for comment in self.__soup(text=lambda x: isinstance(x, Comment)): comment.extract()
        for script in self.__soup.find_all('script', src=False): script.decompose()
        for noscript in self.__soup.find_all('noscript'): noscript.decompose()
        return str(self.__soup.html)

