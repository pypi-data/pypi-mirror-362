class QueryParamsBuilder:
    def __init__(self):
        self.params = {}

    def add_token(self, key, value):
        if value is not None:
            self.params[key] = value
        return self

    def add_payload(self, payload):
        for key, value in payload.items():
            if value is not None:
                self.params[key] = value
        return self

    def build(self):
        return self.params
