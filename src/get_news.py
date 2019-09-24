#!/usr/bin/env python3
# coding: utf8
# PythonでRSSからニュースを取得しSQLite3DBに保存する。
# 第1引数: 必須。RSS URL
# 第2引数: 任意。DB出力ディレクトリパス（デフォルト＝カレントディレクトリ）
import sys
import os
import feedparser
from mod import DateTimeString
from mod import HtmlGetter
from mod import HtmlContentExtractor
from mod import NewsDb
from mod import NewsImagesDb

if len(sys.argv) < 2:
    raise Error('第1引数にRSSのURLを指定してください。')
    exit()
rss = sys.argv[1]
db_dir_path = sys.argv[2] if (2 < len(sys.argv)) else os.getcwd()

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

