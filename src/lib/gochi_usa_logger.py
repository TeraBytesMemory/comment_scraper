#!/usr/bin/env python
# coding: utf-8

from lib.comment_watcher import CommentWatcher
import pymongo


class GochiUsaLogger(CommentWatcher):

    def __init__(self, mail, password):
        super().__init__()

        self.login(mail, password)
        self.access("http://www.nicovideo.jp/watch/1397552685")

    def access_mongo(self, url):
        self.mongo_client = pymongo.MongoClient(url)
        self.db = self.mongo_client['nicovideo']
        self.col = self.db['gochi_usa_comment']

    def save_comment(self, data):
        if self.col:
            exist = self.col.find({
                "_id": {
                    "$in": [d["_id"] for d in data]
                }
            })

            exist_id = [d["_id"] for d in exist]

            new = filter(lambda x: not x["_id"] in exist_id, data)
            new = filter(lambda x: x["date"] and x["time"] and x["comment"],
                         new)
            new = list(new)

            if new:
                self.col.insert_many(new)
                return True
            else:
                self.logging("Fail to add data.")
                return False
        else:
            self.logging("Not found gochi_usa_comment collection.")
            return False

    def scrap_and_save_comment(self):
        comments = self.scrap_comment()
        if comments:
            self.save_comment(comments)
