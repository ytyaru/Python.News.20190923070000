from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from bs4 import Comment
import time
import re

class HtmlGetter:
    def __init__(self):
        self.__moreLinkGetter = MoreLinkGetter()
    def get(self, url, wait_second=1):
        html = self.__get_html(url)
        self.__soup = BeautifulSoup(html, 'html.parser')
#        self.__soup = BeautifulSoup(self.__get_html(url), 'lxml')
#        self.__soup = BeautifulSoup(__get_html(url), 'html.parser')
#        html = self.__get_more_link_html(__get_html(url))
        more_url = self.__moreLinkGetter.get(self.__soup, url)
        if more_url != url: 
            url = more_url 
            html = self.__get_html(url)
            self.__soup = BeautifulSoup(html, 'html.parser')
#        html = self.__get_html(str(self.__soup.html))
        html = self.__del_element(html)
        time.sleep(wait_second)
        return url, html
    def __get_html(self, url):
        options = Options()
        options.set_headless(True)
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
        return driver.page_source.encode('utf-8').decode('utf-8')
#    # 「続きを読む」リンクがあるならそのURLを返す。なければ元のURLを返す
#    def __get_more_link_html(self, html):
#        link = self.__soup.find('a', text=re.compile(r'^.*続きを読む.*$'))
#        return html if link is None else self.__get_html(link.get('href'))
    # 不要な要素を削除する
    def __del_element(self, html):
        self.__soup.find('head').decompose()
        for comment in self.__soup(text=lambda x: isinstance(x, Comment)): comment.extract()
        for script in self.__soup.find_all('script', src=False): script.decompose()
        for noscript in self.__soup.find_all('noscript'): noscript.decompose()
        return str(self.__soup.html)

class MoreLinkGetter:
    def __init__(self): pass
#        self.__url = None
#    @property
#    def Url(self): return self.__url
    def get(self, soup, url):
#        return soup.find('a', text=re.compile(r'^.*続きを読む.*$'))
        link = soup.find('a', text=re.compile(r'^.*続きを読む.*$'))
        return url if link is None else link.get('href')

