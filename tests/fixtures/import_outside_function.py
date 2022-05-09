import requests
from requests import get


class Foo:
    def test(self):
        get("https://google.com")

    def test2(self):
        requests.get("https://google.com")
