import os

import requests
import random
import dotenv

from app import QUANTITY


class SIB:
    url = "https://padlet.com/api/3/wishes"
    __QUANTITY = 0
    __HEADERS = {
        "authorization": os.environ.get("TOKEN"),
    }
    __DATA = {
        "sort_index": "3838739544064",
    }

    @classmethod
    def set_quantity(cls, quantity):
        cls.__QUANTITY = quantity

    @classmethod
    def set_wall_id(cls, wall_id):
        cls.__DATA["wall_id"] = wall_id

    @classmethod
    def set_wall_sec(cls, wall_sec):
        cls.__DATA["wall_section_id"] = wall_sec

    @classmethod
    def add_attachment(cls, url):
        cls.__DATA["attachment"] = url

    @classmethod
    def add_body(cls, body):
        cls.__DATA["body"] = body

    @classmethod
    def add_author_id(cls, author_id):
        cls.__DATA["author_id"] = author_id

    @classmethod
    def add_created_time(cls, time):
        cls.__DATA["created_at"] = time

    @classmethod
    def add_subject(cls, subject):
        cls.__DATA["subject"] = subject 

    @classmethod
    def get_headers(cls):
        return cls.__HEADERS

    @classmethod
    def get_data(cls):

        return cls.__DATA

    @classmethod
    def get_quantity(cls):
        return cls.__QUANTITY

    @classmethod
    def run_attack(cls):
        if "wall_id" not in cls.__DATA.keys():
            raise ConnectionError("no wall_id found")
        for i in range(cls.__QUANTITY):
            message = str(i+1) + "/" + str(cls.__QUANTITY)
            requests.post(cls.url, headers=cls.get_headers(), data=cls.get_data())
            yield message
