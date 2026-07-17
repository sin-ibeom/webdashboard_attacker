import os

import requests
import random

from app import QUANTITY


class SIB:
    message = os.environ.get("TOKEN")
    url = "https://padlet.com/api/3/wishes"
    __QUANTITY = 0
    __HEADERS = {
        "authorization": "TOKEN",
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
    def start(cls):
        if "wall_id" not in cls.__DATA.keys():
            raise ConnectionError("no wall_id found")
        for i in range(cls.__QUANTITY):
            # SIB.add_subject(f"Продам машиноместо N{str(i + 1)}")
            # SIB.add_body(f"{random.randint(200, 1000)}$")
            message = str(i+1) + "/" + str(cls.__QUANTITY)
            requests.post(cls.url, headers=cls.get_headers(), data=cls.get_data())
            yield message


SIB.add_attachment(
    "https://static.wikia.nocookie.net/joke-battles/images/d/d4/What-is-a-computer-virus-"
    "a82f9491ad3644b89446d45233b57761.jpg/revision/latest?cb=20201129021158")
# SIB.set_quantity(20)
# SIB.set_wall_id(267316514)
# SIB.set_wall_sec(379179453)
# SIB.start()
