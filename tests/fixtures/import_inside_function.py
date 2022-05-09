class Foo:
    def test(self):
        from requests import get

        get("https://google.com")

    def test2(self):
        import requests

        requests.get("https://google.com")
