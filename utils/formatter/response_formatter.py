import json


class ResponseFormatter:
    def __init__(self, response):
        self.endpoint = response.request.url
        self.body = json.loads(response.text) if not response.status_code >= 500 else response.text
        self.status_code = response.status_code
