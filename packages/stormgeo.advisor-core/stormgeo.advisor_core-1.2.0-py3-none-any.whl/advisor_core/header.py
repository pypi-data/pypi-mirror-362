class Header:
    def __init__(self, language="en-US"):
        self.headers = {
            "Accept": "application/json",
            "Accept-Language": language,
            "Content-Type": "application/json"
        }
    
    def set(self, key, value):
        self.headers[key] = value

    def get(self, key):
        return self.headers.get(key, None)
    
    def getFormattedHeader(self):
        return self.headers
