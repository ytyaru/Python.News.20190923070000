#!/usr/bin/env python3
# coding: utf8
# PythonでRSSからニュースを取得しSQLite3DBに保存する。
# stdin  : 必須。RSS URL
# 第1引数: 任意。SQLite3DBファイルパス（デフォルト＝カレントディレクトリ/news.db）
# 例1: echo -e 'RSS1\nRSS2\nRSS3' | python3 get_news.py ./news.db
# 例2: cat rss_list_source1.txt   | python3 get_news.py ./news.db
import sys
import os
import feedparser
from mod import DateTimeString
from mod import HtmlGetter
from mod import HtmlContentExtractor
from mod import NewsDb
from mod import NewsImagesDb

rss_list = sys.stdin.readlines() # 標準入力がなければ永久に待機してしまう！
if 0 == len(rss_list):
    raise Error(("stdinにRSSのURLを指定してください。コード例は以下。\n" + 
                "echo 'RSS1' | python3 get_news.py" + 
                "echo -e 'RSS1\nRSS2\nRSS3' | python3 get_news.py ./news.db\n" + 
                "cat rss_list_source1.txt   | python3 get_news.py ./news.db\n" + 
                "第1引数にSQLite3DBファイル出力パスを指定できます。デフォルトは「./news.db」です。"))
    exit()
db_dir_path = sys.argv[1] if (1 < len(sys.argv)) else os.path.join(os.getcwd(), 'news.db')

for rss in rss_list:
    entries = feedparser.parse(rss).entries
    dtcnv = DateTimeString.DateTimeString()
    #extractor = HtmlContentExtractor.HtmlContentExtractor()
    extractor = HtmlContentExtractor.HtmlContentExtractor(option={"threshold":50})
    getter = HtmlGetter.HtmlGetter()
    news_db = NewsDb.NewsDb(db_dir_path)
    for entry in entries:
        # RDF形式のときpublishedがない。代わりにupdatedがある
        published = dtcnv.convert_utc((
                entry.published 
                if hasattr(entry, 'published') 
                else entry.updated)
            ).strftime('%Y-%m-%dT%H:%M:%SZ')
        url = entry.link
        title = entry.title
        if news_db.is_exists(published,url): continue
    #    body = extractor.extract(get_html.get_html(url))
        body = extractor.extract(getter.get(url))
        news_db.append_news(published, url, title, body);
    #    break; # HTML取得を1件だけでやめる
    news_db.insert();

