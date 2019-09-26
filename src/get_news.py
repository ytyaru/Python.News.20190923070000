#!/usr/bin/env python3
# coding: utf8
# PythonでRSSからニュースを取得しSQLite3DBに保存する。
# stdin  : 必須。RSS URL
# 第1引数: 任意。SQLite3DBファイルパス（デフォルト＝カレントディレクトリ/news.db）
# 例1: echo -e 'RSS1\nRSS2\nRSS3' | python3 get_news.py ./news.db
# 例2: cat feeds_source1.txt   | python3 get_news.py ./news.db
import sys
import os
import feedparser
from mod import DateTimeString
from mod import HtmlGetter
from mod import HtmlContentExtractor
from mod import FeedDb
from mod import NewsDb
from mod import NewsImagesDb

feeds = sys.stdin.readlines() # 標準入力がなければ永久に待機してしまう！
if 0 == len(feeds):
    raise Error(("stdinにRSSのURLを指定してください。コード例は以下。\n" + 
                "echo 'RSS1' | python3 get_news.py" + 
                "echo -e 'RSS1\nRSS2\nRSS3' | python3 get_news.py ./news.db\n" + 
                "cat feeds_source1.txt   | python3 get_news.py ./news.db\n" + 
                "第1引数にSQLite3DBファイル出力パスを指定できます。デフォルトは「./news.db」です。"))
    exit()
db_dir_path = sys.argv[1] if (1 < len(sys.argv)) else os.path.join(os.getcwd(), 'news.db')

def has_def(obj, attr, default): 
    return getattr(obj, attr) if hasattr(obj, attr) else default

# フィードのみ取得
feed_db_path = '/tmp/work/feeds.db'
os.makedirs(os.path.dirname(feed_db_path), exist_ok=True)
dtcnv = DateTimeString.DateTimeString()
feed_db = FeedDb.FeedDb('/tmp/work/feeds.db')
for feed in feeds:
    entries = feedparser.parse(feed).entries
    for entry in entries:
        published = dtcnv.convert_utc((
            has_def(entry, 'published', entry.updated))
            ).strftime('%Y-%m-%dT%H:%M:%SZ')
        url = entry.link
        title = entry.title
        summary = has_def(entry, 'summary', '')
        feed_db.append_news(published,url,title,summary=summary)
    feed_db.insert() # :memory:へ
feed_db.marge() # 指定パスへ

# 取得したフィードのうちDB内の最新日時より新しいエントリのみ取得する
news_db = NewsDb.NewsDb(db_dir_path)
newer_entries = feed_db.get_news(news_db.LatestPublished)
print('len(newer_entries): {}'.format(len(newer_entries)))

# ファイルDBへ挿入する（本文抽出も）
extractor = HtmlContentExtractor.HtmlContentExtractor(option={"threshold":50})
getter = HtmlGetter.HtmlGetter()
for entry in newer_entries:
    url, html = getter.get(entry['url']) # 「続きを読む」があればURLが変わる
    body = extractor.extract(html)
#    body = extractor.extract(getter.get(entry['url']))
    news_db.append_news(entry['published'], url, entry['title'], body);
news_db.insert();

"""
# 本文抽出
for rss in feeds:
    entries = feedparser.parse(rss).entries
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
        body = extractor.extract(getter.get(url))
        news_db.append_news(published, url, title, body);
    #    break; # HTML取得を1件だけでやめる
    news_db.insert();
"""

