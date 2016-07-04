#!/usr/bin/env python
# coding: utf-8

from lib.gochi_usa_logger import GochiUsaLogger
from time import sleep
import os


mail = os.environ['NICO_MAIL'] # 環境変数で設定。ニコニコ動画の登録メールアドレス
password = os.environ['NICO_PASS'] # 環境変数で設定。ニコニコ動画の登録パスワード
mongo_url = "localhost:27017"
scrollTo = 62000
scrollUp = 200
wait_time = 3


if __name__ == '__main__':
    logger = GochiUsaLogger(mail, password)

    logger.access_mongo(mongo_url)

    while scrollTo > 0:
        comment = logger.scrap_comment()

        if comment:
            logger.save_comment(comment)
            logger.scroll_comment_list(scrollUp)
            scrollTo -= scrollUp

        sleep(wait_time)
