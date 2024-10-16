# error.py
from models import base

class DanaError(base.APIBase):
    """Basis kelas error untuk semua error yang terkait dengan DANA"""
    def __init__(self, code, status, message):
        self.code = code
        self.status = status
        self.message = message

class DanaAPIError(Exception):
    """Basis kelas error untuk semua error yang terkait dengan DANA API"""
    pass

class DanaNotLoggedIn(DanaAPIError):
    """Error yang terjadi saat pengguna tidak terotentikasi di DANA"""
    def __init__(self, code, status, message):
        self.code = code
        self.status = status
        self.message = message

class DanaUsageError(DanaAPIError):
    """Error yang terjadi saat ada masalah dengan penggunaan DANA"""
    def __init__(self, code, status, message):
        self.code = code
        self.status = status
        self.message = message

class DanaHttpResponse(DanaAPIError):
    """Kelas untuk menyimpan respons dari DANA"""
    def __init__(self, code, status, message, content, data):
        self.code = code
        self.status = status
        self.message = message
        self.content = content
        self.data = data

class DanaAmountException(DanaAPIError):
    """Error yang terjadi saat ada masalah dengan jumlah yang dimasukkan"""
    def __init__(self, code, status, message):
        self.code = code
        self.status = status
        self.message = message

class DanaUnexpectedError(DanaAPIError):
    """Error yang terjadi saat ada masalah yang tidak terduga di DANA"""
    def __init__(self, code, status, message):
        self.code = code
        self.status = status
        self.message = message