# base.py

class BaseResponse:
    def __init__(self, code, status, message):
        self.code = code
        self.status = status
        self.message = message

    def __getitem__(self, key):
        return getattr(self, key, None)

    def __setitem__(self, key, val):
        return setattr(self, key, val)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def __eq__(self, obj):
        return self.__class__.__name__ == obj.__class__.__name__

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    __str__ = __repr__

class BaseError(Exception):
    def __init__(self, code, status, message):
        self.code = code
        self.status = status
        self.message = message
        super().__init__(message)

class APIBase:
    def __init__(self):
        self.api_url = 'https://api.dana.id/'
        self.api_key = 'https://api.dana.id/'
        self.api_secret = 'YOUR_API_SECRET'

    def make_request(self, method, endpoint, data=None):
        # Implementasi untuk membuat request ke API
        pass

    def handle_response(self, response):
        # Implementasi untuk menangani respons dari API
        pass

class Request(BaseResponse):
    pass