import requests, re

def validate_url(url):
    """validate and correct an url"""
    pattern = r"^https?:\/\/(?:www\.)?[a-zA-Z0-9.-]+(?:\:[0-9]+)?(?:\/.*)?$"
    pattern_no = r"^(?:www\.)?[a-zA-Z0-9.-]+(?:\:[0-9]+)?(?:\/.*)?$"
    if not re.match(pattern, url):
        if re.match(pattern_no, url):
            return "http://" + url
        else:
            return False
    else:
        return url


class Test:
    class Response:
        """the response class"""
        json = {}
        cookie = {}
        text = ""
        headers = {}
        status_code = 0

    class Request:
        """the request class"""
        url = ""
        method = ""
        json = {}
        cookie = {}
        headers = {}

    def __init__(self, url: str, method = "GET", json: dict = None, form: dict = None, headers = {}, cookie = {}):
        if not validate_url(url):
            ValueError(f"url formatting is wrong({url})")

        self._run = []
        self.body = False

        if json:
            if not validate_url(url):
                self.body = True
            else:
                ValueError("Too many arguments")

        if form:
            if not self.body:
                self.body = True
            else:
                ValueError("Too many arguments")

        if self.body:
            if json:
                self.request = requests.request(method, validate_url(url), json=json, headers=headers, cookies=cookie)
            if form:
                self.request = requests.request(method, validate_url(url), data=form, headers=headers, cookies=cookie)
        else:
            self.request = requests.request(method, validate_url(url), headers=headers, cookies=cookie)


        try:
            self.Response.json = self.request.json()
        except ValueError:
            self.Response.json = {}

        self.Response.cookie = self.request.cookies
        self.Response.status_code = self.request.status_code
        self.Response.headers = self.request.headers
        self.Response.text = self.request.text

        self.Request.url = url
        self.Request.method = method
        self.Request.json = json
        self.Request.cookie = cookie
        self.Request.headers = headers

    def test(self, name):
        """used to declare a test function, the function you use this on must return True or False.
        run the function with a testinstance argument that contain the Request and Response class plus the requestc class for advanced testing."""
        def wrapper(func):
            def wrapped_func():
                try:
                    resp = func(testinstance=self)
                    if resp is True:
                        print("Passed | " + name)
                    else:
                        print("Failed | " + name)
                except Exception as e:
                    print(f"Error during test: {e} | {name}")
            self._run.append(wrapped_func)
            return wrapped_func
        return wrapper

    def run(self):
        """runs all the test"""
        for functions in self._run:
            functions()