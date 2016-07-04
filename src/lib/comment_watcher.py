#!/usr/bin/env python
# coding: utf-8

from lib.nicovideo_watcher import NicoVideoWatcher

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from logging import debug


class CommentWatcher(NicoVideoWatcher):

    def __init__(self):
        super().__init__()

    def scrap_comment(self):
        comments = []

        try:
            comment_elm = WebDriverWait(self.driver, 40).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                     ".slick-cell.l0.r0"))
            )

            comment_context = [c.text for c in comment_elm]
            comment_parent = [c.find_element_by_xpath("..") for c in comment_elm]

            comments = map(lambda context, elm: {
                "comment": context,
                "time": elm.find_element_by_css_selector(".slick-cell.l1.r1").text,
                "date": elm.find_element_by_css_selector(".slick-cell.l2.r2").text,
                "_id": elm.find_element_by_css_selector(".slick-cell.l3.r3").text,
            }, comment_context, comment_parent)

            comments = filter(lambda x: x["date"] and x["time"] and x["comment"], comments)
            comments = list(comments)

            for c in comments:
                self.logging("Acces to the comment {0:s}".format(c["_id"]))

        except:
            self.logging_exception("Can not access comments")

        finally:
            return comments

    def scroll_comment_list(self, scrollUp=300):
        cls = "slick-viewport"

        script = "document.getElementsByClassName('{0:s}')[0].scrollTop -= {1:d};".format(cls, scrollUp)

        self.driver.execute_script(script)
        self.driver.implicitly_wait(5)

    def reload_comment(self):
        self.driver.find_element_by_css_selector(".header-icon.refresh.on").click()
