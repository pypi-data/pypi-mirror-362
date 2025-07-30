import requests
import time

class RequestHandler:
    def __init__(self, base_url, token, retries, delay, headers):
        self.base_url = base_url
        self.token = token
        self.retries = retries
        self.delay = delay
        self.session = requests.Session()
        self.headers = headers

    def make_request(self, method, endpoint, params=None, json_data=None, retries=None, stream=False):
        retries = retries if retries is not None else self.retries
        full_url = f"{self.base_url}{endpoint}"
        error_message = ''

        try:
            headers = self.headers.getFormattedHeader()
            if method == "GET":
                response = self.session.get(full_url, params=params, headers=headers, stream=stream)
            elif method == "POST":
                response = self.session.post(full_url, params=params, json=json_data, headers=headers)
            else:
                response = self.session.request(method, full_url, json=json_data, headers=headers)

            status = response.status_code

            if status != 200 and status is not None:
                if self.headers.get("Accept") != "application/json":
                    error_message = response.text
                else:
                    error_message = response.json().get("error", response.text)
                
                if status < 500 and status != 429:
                    return {"data": None, "error": error_message}

            response.raise_for_status()

            if stream:
                return {
                    "data": response.iter_content(chunk_size=8192),
                    "response": response,
                    "error": None
                }

            content_type = response.headers.get("Content-Type", "")
            if not content_type.startswith("application/json"):
                return {"data": response.content, "error": None}

            return {
                "data": response.text if self.headers.get("Accept") != "application/json" else response.json(),
                "error": None,
            }

        except requests.exceptions.RequestException as error:
            if retries > 0:
                time.sleep(self.delay)
                print(f"Re-trying in {self.delay}s... attempts left: {retries}")
                return self.make_request(method, endpoint, params, json_data, retries - 1, stream=stream)

            return {
                "data": None,
                "error": error_message if error_message != '' else error,
            }
