from .base import BaseResponse as Response
import hashlib


class Auth:
    def __init__(self):
        self.users = {}

    def register(self, username, password):
        # hash password menggunakan SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.users[username] = hashed_password

    def login(self, username, password):
        # hash password menggunakan SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if username in self.users and self.users[username] == hashed_password:
            return True
        else:
            return False

    def logout(self, username):
        # tidak perlu implementasi karena tidak ada session
        pass


class LoginWithToken(Response):
    def __init__(self, auth):
        super().__init__()
        self.auth = auth

    def read(self, MapObject):
        username = MapObject.get('username', None)
        password = MapObject.get('password', None)
        if self.auth.login(username, password):
            self.success = True
        else:
            self.success = False


class Login2FAResponse(Response):
    def __init__(self, auth):
        super().__init__()
        self.auth = auth

    def read(self, MapObject):
        # implementasi 2FA
        username = MapObject.get('username', None)
        password = MapObject.get('password', None)
        if self.auth.login(username, password):
            # generate kode OTP
            otp_code = self.auth.generate_otp_code(username)
            # kirim kode OTP ke pengguna melalui SMS atau email
            self.auth.send_otp_code(otp_code, username)
            self.refId = otp_code
        else:
            self.success = False


class Login2FAVerifyResponse(Response):
    def __init__(self, auth):
        super().__init__()
        self.auth = auth

    def read(self, MapObject):
        # implementasi verifikasi 2FA
        username = MapObject.get('username', None)
        otp_code = MapObject.get('otp_code', None)
        if self.auth.verify_otp_code(username, otp_code):
            self.success = True
        else:
            self.success = False


class LoginSecurityCodeResponse(Response):
    def __init__(self, auth):
        super().__init__()
        self.auth = auth

    def read(self, MapObject):
        # implementasi security code
        username = MapObject.get('username', None)
        security_code = MapObject.get('security_code', None)
        if self.auth.verify_security_code(username, security_code):
            self.success = True
        else:
            self.success = False


class LogoutResponse(Response):
    def __init__(self, auth):
        super().__init__()
        self.auth = auth

    def read(self, MapObject):
        # tidak perlu implementasi karena tidak ada session
        pass