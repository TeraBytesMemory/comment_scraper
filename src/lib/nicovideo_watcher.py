#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from datetime import datetime
import logging as _logging
from os import path


class NicoVideoWatcher(object):
    login_url = 'http://www.nicovideo.jp/login'

    def __init__(self):
        self.driver = webdriver.Chrome()

        _logging.basicConfig(filename=path.join('/tmp/' 'gochi_usa_info.log'),
                             filemode='a',
                             level=_logging.INFO)

    def __del__(self):
        self._quit()

    def login(self, mail, password):
        self.driver.get(self.login_url)

        self.driver.find_element_by_id("input__mailtel").send_keys(mail)
        self.driver.find_element_by_id("input__password").send_keys(password)
        self.driver.find_element_by_id("login__submit").click()

    def access(self, url):
        try:
            self.driver.get(url)
        except Exception:
            self.logging_exception("Cannot access")
        else:
            self.logging("Access to {0:s}".format(url))

    def _quit(self):
        self.driver.quit()

    def logging(self, log, func=_logging.info):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        func('[%s] %s', now, log)

    def logging_exception(self, log):
        log = "[Exception]" + log
        self.logging(log, _logging.exception)

    def screen_only_element(self, elm):
        self.driver.execute_script("window.scrollBy({0},{1})".format(
            elm.location["x"], elm.location["y"])
        );
        self.driver.set_window_size(elm.size["width"], elm.size["height"])
